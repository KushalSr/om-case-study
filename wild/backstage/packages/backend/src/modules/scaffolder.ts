import {
  coreServices,
  createBackendModule,
} from '@backstage/backend-plugin-api';
import { scaffolderActionsExtensionPoint } from '@backstage/plugin-scaffolder-node/alpha';

import { createCustomAction } from '../actions/customAction';

export const scaffolderModuleCustomAction = createBackendModule({
  pluginId: 'scaffolder',
  moduleId: 'custom-action',

  register(env) {
    env.registerInit({
      deps: {
        scaffolder: scaffolderActionsExtensionPoint,
        logger: coreServices.logger,
      },

      async init({ scaffolder, logger }) {
        scaffolder.addActions(createCustomAction());

        logger.info('Registered my:custom:action');
      },
    });
  },
});