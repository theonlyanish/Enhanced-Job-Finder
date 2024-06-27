import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface Job {
  id: string;
  title: string;
  company: string;
  salary?: string;
  date?: string;
  type: string;
  seen: boolean;
  link: string;
}

interface JobsState {
  list: Job[];
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

const initialState: JobsState = {
  list: [],
  status: 'idle',
  error: null,
};

export const fetchJobs = createAsyncThunk('jobs/fetchJobs', async (_, { getState }) => {
  // In a real application, you'd make an API call here
  // For now, we'll just return some mock data
  const mockJobs: Job[] = [
    {
      id: '1',
      title: 'Frontend Developer',
      company: 'TechCorp',
      salary: '$80,000 - $120,000',
      date: '2023-06-01',
      type: 'Full-time',
      seen: false,
      link: 'https://example.com/job1',
    },
    {
      id: '2',
      title: 'Backend Engineer',
      company: 'DataSystems',
      salary: '$90,000 - $130,000',
      date: '2023-05-28',
      type: 'Full-time',
      seen: false,
      link: 'https://example.com/job2',
    },
    // Add more mock jobs as needed
  ];

  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  return mockJobs;
});

const jobsSlice = createSlice({
  name: 'jobs',
  initialState,
  reducers: {
    markJobAsSeen: (state, action: PayloadAction<string>) => {
      const job = state.list.find(job => job.id === action.payload);
      if (job) {
        job.seen = true;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchJobs.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchJobs.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.list = action.payload;
      })
      .addCase(fetchJobs.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message || 'Something went wrong';
      });
  },
});

export const { markJobAsSeen } = jobsSlice.actions;

export default jobsSlice.reducer;