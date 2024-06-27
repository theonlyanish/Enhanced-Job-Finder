'use client';
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { setKeywordInclusion, setKeywordExclusion, setKeywordInclusionDesc, setKeywordExclusionDesc } from '../store/filtersSlice';
import { fetchJobs } from '../store/jobsSlice';
import { RootState, AppDispatch } from '../store';

const SearchForm: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const filters = useSelector((state: RootState) => state.filters);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(fetchJobs());
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onSubmit={handleSubmit}
      className="space-y-4 mb-8"
    >
      <div>
        <input
          type="text"
          placeholder="Keywords to include in title"
          value={filters.keywordInclusion}
          onChange={(e) => dispatch(setKeywordInclusion(e.target.value))}
          className="input"
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Keywords to exclude from title"
          value={filters.keywordExclusion}
          onChange={(e) => dispatch(setKeywordExclusion(e.target.value))}
          className="input"
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Keywords to include in description"
          value={filters.keywordInclusionDesc}
          onChange={(e) => dispatch(setKeywordInclusionDesc(e.target.value))}
          className="input"
        />
      </div>
      <div>
        <input
          type="text"
          placeholder="Keywords to exclude from description"
          value={filters.keywordExclusionDesc}
          onChange={(e) => dispatch(setKeywordExclusionDesc(e.target.value))}
          className="input"
        />
      </div>
      <button type="submit" className="btn">
        Search
      </button>
    </motion.form>
  );
};

export default SearchForm;