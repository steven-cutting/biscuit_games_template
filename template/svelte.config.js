import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/**
 * The game is a static site with no server, so every route is prerendered and
 * the build output is a directory of files a host can serve as-is.
 *
 * `paths.base` places a project site under BASE_PATH, set by pages.yml from the
 * repository name; empty locally.
 */

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({ pages: 'build', assets: 'build', strict: true }),
    paths: { base: process.env.BASE_PATH ?? '' },
    typescript: {
      /**
       * SvelteKit generates `.svelte-kit/tsconfig.json` covering `src`, `test`,
       * `tests` and `vite.config.*`. The root `tsconfig.json` extends it, and a
       * derived config's `include` replaces the inherited one rather than adding
       * to it, so the workshop is added here instead of there. Without this,
       * `.storybook/`, `stories/` and `vitest.storybook.config.ts` belong to no
       * TypeScript project: `svelte-check` skips them silently and
       * typescript-eslint's project service fails outright. Paths are relative
       * to the generated file.
       */
      config: (generated) => {
        generated.include.push(
          '../.storybook/**/*.ts',
          '../stories/**/*.ts',
          '../stories/**/*.svelte',
          '../vitest.storybook.config.ts'
        );
      }
    }
  }
};

export default config;
