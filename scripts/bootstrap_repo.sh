#!/bin/sh
set -eu

# Applies the repository settings a rendered game needs and no file can carry.
# Read, compare, mutate: without --apply nothing changes and every step prints
# the command it would run; with --apply a second run changes nothing.
#
# The step numbers are fixed, and are the ones
# tickets/C03-repository-bootstrap.md and README.md's "Bootstrap a repository"
# use: --no-pages omits step 1 rather than renumbering the rest.

usage() {
  cat >&2 <<'USAGE'
usage:
  scripts/bootstrap_repo.sh <owner>/<repo> [--apply] [--checks a,b,c]
                            [--no-pages] [--chromatic-token-stdin] [--hygiene]
USAGE
  exit 2
}

die() {
  printf '%s\n' "$*" >&2
  exit 1
}

# An option's value is an argument error, so it exits 2 as a bad option does,
# and not 1, which this script keeps for a `gh` call that failed.
bad_option() {
  printf '%s\n' "$*" >&2
  exit 2
}

repo=''
apply=''
# The check names a game's `ci.yml` produces, one per job of the shared workflow
# it calls: `<caller job> / <called job>`. They carry spaces, so the list is
# split on commas alone and is never trimmed.
checks='ci / frontend,ci / documents,ci / stories'
pages=1
token_stdin=''
hygiene=''

while [ "$#" -gt 0 ]; do
  case $1 in
    --apply) apply=1 ;;
    --checks)
      [ "$#" -ge 2 ] || usage
      checks=$2
      shift
      ;;
    --checks=*) checks=${1#--checks=} ;;
    --no-pages) pages='' ;;
    --chromatic-token-stdin) token_stdin=1 ;;
    --hygiene) hygiene=1 ;;
    -*) usage ;;
    *)
      [ -z "$repo" ] || usage
      repo=$1
      ;;
  esac
  shift
done

[ -n "$repo" ] || usage
# <owner>/<repo>: one slash, neither side empty, nothing exotic on either.
case $repo in
  */*/* | /* | */) usage ;;
  */*) ;;
  *) usage ;;
esac
case $repo in
  *[!A-Za-z0-9._/-]*) usage ;;
esac

# Splits a comma-separated list onto one line each. Globbing is off across the
# split so a name is never expanded against the working directory, and nothing
# is trimmed: `ci / frontend` is one name, spaces included.
split_commas() {
  list=$1
  # Checked before the split, because an empty value splits into no fields at
  # all and would reach the body as an empty `checks` array, removing every
  # required check rather than being refused.
  case $list in
    '') bad_option '--checks: the list is empty' ;;
    ,* | *,) bad_option "--checks: '$list' has a leading or trailing comma" ;;
    *,,*) bad_option "--checks: '$list' has two commas in a row" ;;
  esac
  set -f
  IFS=','
  # shellcheck disable=SC2086 # deliberate: word splitting on commas alone
  set -- $list
  set +f
  unset IFS
  for one in "$@"; do
    [ -n "$one" ] || bad_option "--checks: empty check name in '$list'"
    case $one in
      *'"'* | *\\*) bad_option "--checks: '$one' carries a quote or a backslash" ;;
    esac
  done
  printf '%s\n' "$@"
}

check_lines=$(split_commas "$checks")
# jq's `sort` orders by codepoint, so the expected line is built the same way.
checks_sorted=$(printf '%s\n' "$check_lines" | LC_ALL=C sort | tr '\n' ',')
checks_sorted=${checks_sorted%,}

err=$(mktemp)
trap 'rm -f "$err"' EXIT
trap 'rm -f "$err"; exit 1' INT TERM

# Set by gh_read, which cannot hand them back through a command substitution:
# the subshell one creates would swallow read_status.
read_out=''
read_status=''
changed=0

# Runs a read, and reports an HTTP status the caller treats as a state rather
# than a failure. `gh` writes the error body to stdout even under --jq, so on a
# non-zero exit the captured stdout is discarded and the status is taken from
# the message on stderr. A bare non-zero exit (an expired login, a network
# fault) is never read as "not enabled".
gh_read() {
  read_out=''
  read_status=''
  if read_out=$(gh "$@" 2>"$err"); then
    return 0
  fi
  if grep -q '(HTTP 404)' "$err"; then
    read_status=404
    return 1
  fi
  cat "$err" >&2
  die "gh $* failed"
}

step() {
  printf '\n%s. %s\n' "$1" "$2"
}

state() {
  printf '   state: %s\n' "$1"
}

note() {
  printf '   %s\n' "$1"
}

# Prints a mutation and counts it. The caller runs the command itself, because
# several of them need a heredoc or a pipe.
announce() {
  if [ -n "$apply" ]; then
    printf '   + %s\n' "$1"
  else
    printf '   would: %s\n' "$1"
  fi
  changed=$((changed + 1))
}

# `build_type` alone has been accepted by both verbs on every repository tried.
# Where an older Pages API demands a source, the documented body carries one, and
# the fallback says so rather than aborting.
pages_with_source() {
  note "HTTP 422: the API asks for a source, so the $1 is resent with one"
  printf '   + %s\n' "gh api -X $1 repos/$repo/pages --input - (with a main / source)"
  printf '%s\n' '{"build_type": "workflow", "source": {"branch": "main", "path": "/"}}' |
    gh api -X "$1" "repos/$repo/pages" --input - >/dev/null
}

pages_put() {
  if ! gh api -X PUT "repos/$repo/pages" -f build_type=workflow >/dev/null 2>"$err"; then
    grep -q '(HTTP 422)' "$err" || {
      cat "$err" >&2
      die 'gh api -X PUT pages failed'
    }
    pages_with_source PUT
  fi
}

printf 'repository: %s\n' "$repo"
if [ -n "$apply" ]; then
  printf 'mode: apply\n'
else
  printf 'mode: dry run (nothing is changed)\n'
fi

# 1. The Pages source. The workflow cannot set this for itself: until it is
#    GitHub Actions the build uploads its artefact and the deploy job fails with
#    `Failed to create deployment (status: 404)`.
if [ -n "$pages" ]; then
  step 1 'Pages source'
  if gh_read api "repos/$repo/pages" --jq .build_type; then
    build_type=$read_out
  else
    build_type=''
  fi
  if [ "$build_type" = workflow ]; then
    state 'workflow'
    note 'already'
  elif [ "$read_status" = 404 ]; then
    state 'no Pages site (HTTP 404)'
    announce "gh api -X POST repos/$repo/pages -f build_type=workflow"
    if [ -n "$apply" ]; then
      if ! gh api -X POST "repos/$repo/pages" -f build_type=workflow >/dev/null 2>"$err"; then
        if grep -q '(HTTP 409)' "$err"; then
          note 'HTTP 409: a site exists already, so the PUT sets the source instead'
          printf '   + %s\n' "gh api -X PUT repos/$repo/pages -f build_type=workflow"
          pages_put
        elif grep -q '(HTTP 422)' "$err"; then
          pages_with_source POST
        else
          cat "$err" >&2
          die 'gh api -X POST pages failed'
        fi
      fi
    fi
  else
    state "$build_type"
    announce "gh api -X PUT repos/$repo/pages -f build_type=workflow"
    [ -z "$apply" ] || pages_put
  fi
fi

# 2. Protection on `main`: the required checks, not required to be up to date,
#    no review, force pushes and deletion refused, administrators not bound. The
#    read takes the names from `checks`, the field the body below writes, and not
#    from the deprecated `contexts` GitHub still mirrors.
step 2 "Protection on main requiring $checks"
protection_read='[
  .required_status_checks.strict,
  ([.required_status_checks.checks[]?.context] | sort | join(",")),
  .enforce_admins.enabled,
  .allow_force_pushes.enabled,
  .allow_deletions.enabled,
  (.required_pull_request_reviews != null),
  (.restrictions != null)
] | map(tostring) | join(" ")'
want="false $checks_sorted false false false false false"
if gh_read api "repos/$repo/branches/main/protection" --jq "$protection_read"; then
  got=$read_out
else
  got='not protected (HTTP 404)'
fi
state "$got"
if [ "$got" = "$want" ]; then
  note 'already'
else
  note "wanted: $want"
  announce "gh api -X PUT repos/$repo/branches/main/protection --input -"
  # `checks` without `app_id` lets GitHub bind each context to the app that
  # reports it, which is GitHub Actions for every check named here.
  body='{
  "required_status_checks": {
    "strict": false,
    "checks": ['
  first=1
  while IFS= read -r one; do
    [ -n "$one" ] || continue
    if [ -n "$first" ]; then
      first=''
    else
      body="$body,"
    fi
    body="$body
      { \"context\": \"$one\" }"
  done <<EOF
$check_lines
EOF
  body="$body
    ]
  },
  \"enforce_admins\": false,
  \"required_pull_request_reviews\": null,
  \"restrictions\": null,
  \"allow_force_pushes\": false,
  \"allow_deletions\": false
}"
  printf '%s\n' "$body" | sed 's/^/     /'
  if [ -n "$apply" ]; then
    printf '%s\n' "$body" |
      gh api -X PUT "repos/$repo/branches/main/protection" --input - >/dev/null
  fi
fi

# 3. CHROMATIC_PROJECT_TOKEN, the one stored secret, and optional: without it
#    the shared Chromatic workflow notes the absence and skips the publish.
step 3 'CHROMATIC_PROJECT_TOKEN'
if ! secret_names=$(gh secret list -R "$repo" --json name --jq '.[].name' 2>"$err"); then
  cat "$err" >&2
  die 'gh secret list failed'
fi
secret=''
case "
$secret_names
" in
  *'
CHROMATIC_PROJECT_TOKEN
'*) secret=1 ;;
esac
if [ -n "$secret" ]; then
  state 'set'
else
  state 'not set'
fi
if [ -z "$token_stdin" ]; then
  if [ -n "$secret" ]; then
    note 'already'
  else
    note 'skipped: no token supplied; chromatic.yml notes the absence and skips the publish'
  fi
else
  announce "gh secret set CHROMATIC_PROJECT_TOKEN -R $repo (value read from stdin)"
  if [ -n "$apply" ]; then
    # One line from stdin, through a builtin: the token is never an argument,
    # never echoed and never written to a file.
    chromatic_token=''
    IFS= read -r chromatic_token || true
    [ -n "$chromatic_token" ] || bad_option '--chromatic-token-stdin: no token on stdin'
    printf '%s' "$chromatic_token" |
      gh secret set CHROMATIC_PROJECT_TOKEN -R "$repo" >/dev/null
    chromatic_token=''
  fi
fi

# 4. Private vulnerability reporting, which the seed SECURITY.md promises.
#    GitHub offers it on public repositories; where it does not exist the policy
#    still names a route, and the message says so.
step 4 'Private vulnerability reporting'
if gh_read api "repos/$repo/private-vulnerability-reporting" --jq .enabled; then
  enabled=$read_out
else
  enabled=''
fi
if [ "$enabled" = true ]; then
  state 'true'
  note 'already'
elif [ "$read_status" = 404 ]; then
  state 'no such endpoint (HTTP 404)'
  note "not available: the repository is private; SECURITY.md's fallback is the route"
else
  state "$enabled"
  announce "gh api -X PUT repos/$repo/private-vulnerability-reporting"
  [ -z "$apply" ] || gh api -X PUT "repos/$repo/private-vulnerability-reporting" >/dev/null
fi

# 5. The package's read grant. No REST endpoint exists for it, and reading the
#    package at all needs a read:packages scope this token does not carry, so
#    this step is printed and never run.
step 5 'Package read access for @steven-cutting/biscuit-games'
state 'cannot be read: no REST endpoint, and the package needs a read:packages scope'
note "The package is public, so any repository installs it with the run's own"
note 'token and no grant is needed. Were it made private, the grant is by hand:'
note 'open the package page, Package settings, Manage Actions access, Add'
note "repository, search for $repo, and set its Role to Read."

# 6. Hygiene, opt-in: delete a branch on merge, and turn off two features
#    neither repository uses.
step 6 'Hygiene'
if [ -z "$hygiene" ]; then
  state 'not read'
  note 'skipped: --hygiene not given'
else
  if ! gh_read api "repos/$repo" \
    --jq '[.delete_branch_on_merge, .has_wiki, .has_projects] | map(tostring) | join(" ")'; then
    die "gh api repos/$repo answered HTTP 404"
  fi
  state "$read_out"
  if [ "$read_out" = 'true false false' ]; then
    note 'already'
  else
    note 'wanted: true false false'
    announce "gh repo edit $repo --delete-branch-on-merge --enable-wiki=false --enable-projects=false"
    [ -z "$apply" ] || gh repo edit "$repo" \
      --delete-branch-on-merge --enable-wiki=false --enable-projects=false >/dev/null
  fi
fi

if [ -n "$apply" ]; then
  printf '\nchanged: %s\n' "$changed"
else
  printf '\nchanged: 0 (dry run; %s would change)\n' "$changed"
fi
