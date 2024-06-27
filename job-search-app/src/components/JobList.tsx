'use client';
import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { motion } from 'framer-motion';
import { fetchJobs } from '../store/jobsSlice';
import JobCard from './JobCard';
import { RootState, AppDispatch } from '../store';

const JobList: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const jobs = useSelector((state: RootState) => state.jobs.list);
  const jobStatus = useSelector((state: RootState) => state.jobs.status);

  useEffect(() => {
    if (jobStatus === 'idle') {
      dispatch(fetchJobs());
    }
  }, [jobStatus, dispatch]);

  if (jobStatus === 'loading') {
    return <div className="text-center">Loading...</div>;
  }

  if (jobStatus === 'failed') {
    return <div className="text-center text-red-500">Error loading jobs</div>;
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ staggerChildren: 0.1 }}
    >
      {jobs.map((job) => (
        <motion.div
          key={job.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <JobCard job={job} />
        </motion.div>
      ))}
    </motion.div>
  );
};

export default JobList;