let interceptorReady = false;
let readyPromise: Promise<void> | null = null;
let resolveReady: (() => void) | null = null;

export function createInterceptorReadySignal() {
  return {
    waitForInterceptor: () => {
      if (interceptorReady) return Promise.resolve();
      if (!readyPromise) {
        readyPromise = new Promise<void>(resolve => {
          resolveReady = resolve;
        });
      }
      return readyPromise;
    },
    markInterceptorReady: () => {
      interceptorReady = true;
      if (resolveReady) resolveReady();
    }
  };
}

export const { waitForInterceptor, markInterceptorReady } = createInterceptorReadySignal();
