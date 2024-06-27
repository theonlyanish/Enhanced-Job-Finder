import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface FiltersState {
  keywordInclusion: string;
  keywordExclusion: string;
  companyBlacklist: string[];
  keywordInclusionDesc: string;
  keywordExclusionDesc: string;
}

const initialState: FiltersState = {
  keywordInclusion: '',
  keywordExclusion: '',
  companyBlacklist: [],
  keywordInclusionDesc: '',
  keywordExclusionDesc: '',
};

const filtersSlice = createSlice({
  name: 'filters',
  initialState,
  reducers: {
    setKeywordInclusion: (state, action: PayloadAction<string>) => {
      state.keywordInclusion = action.payload;
    },
    setKeywordExclusion: (state, action: PayloadAction<string>) => {
      state.keywordExclusion = action.payload;
    },
    addCompanyToBlacklist: (state, action: PayloadAction<string>) => {
      state.companyBlacklist.push(action.payload);
    },
    removeCompanyFromBlacklist: (state, action: PayloadAction<string>) => {
      state.companyBlacklist = state.companyBlacklist.filter(
        company => company !== action.payload
      );
    },
    setKeywordInclusionDesc: (state, action: PayloadAction<string>) => {
      state.keywordInclusionDesc = action.payload;
    },
    setKeywordExclusionDesc: (state, action: PayloadAction<string>) => {
      state.keywordExclusionDesc = action.payload;
    },
    resetFilters: (state) => {
      return initialState;
    },
  },
});

export const {
  setKeywordInclusion,
  setKeywordExclusion,
  addCompanyToBlacklist,
  removeCompanyFromBlacklist,
  setKeywordInclusionDesc,
  setKeywordExclusionDesc,
  resetFilters,
} = filtersSlice.actions;

export default filtersSlice.reducer;