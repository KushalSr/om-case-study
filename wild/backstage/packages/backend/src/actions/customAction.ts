import { resolveSafeChildPath } from '@backstage/backend-plugin-api';
import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import fs from 'fs-extra';
import { z } from 'zod';

export const createCustomAction = () => {
  return createTemplateAction({
    id: 'my:custom:action',
    description: 'Creates a new file in the template workspace',
    schema: {
      input: {
        filename: z.string({
          description: 'The name of the file to create',
        }),
        content: z.string({
          description: 'The content to write to the file',
        }),
      },
    },
    async handler(ctx) {
      const filePath = resolveSafeChildPath(
        ctx.workspacePath,
        ctx.input.filename,
      );

      await fs.outputFile(filePath, ctx.input.content);

      ctx.logger.info(`Created file: ${ctx.input.filename}`);
    },
  });
};