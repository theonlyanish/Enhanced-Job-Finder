import { configureStore } from '@reduxjs/toolkit';
import jobsReducer from './jobsSlice';
import filtersReducer from './filtersSlice';

export const store = configureStore({
  reducer: {
    jobs: jobsReducer,
    filters: filtersReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;