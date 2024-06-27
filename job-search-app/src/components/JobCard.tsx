'use client';
 
import React from 'react';
import { motion } from 'framer-motion';
import { useDispatch } from 'react-redux';
import { markJobAsSeen } from '../store/jobsSlice';

interface JobCardProps {
  job: {
    id: string;
    title: string;
    company: string;
    salary?: string;
    date?: string;
    type: string;
    seen: boolean;
    link: string;
  };
}

const JobCard: React.FC<JobCardProps> = ({ job }) => {
  const dispatch = useDispatch();

  const handleClick = () => {
    dispatch(markJobAsSeen(job.id));
    window.open(job.link, '_blank');
  };

  return (
    <motion.div
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.98 }}
      className="bg-white shadow-md rounded-lg p-6 mb-4 cursor-pointer"
      onClick={handleClick}
    >
      <h3 className="text-lg font-semibold text-gray-800">{job.title}</h3>
      <p className="text-gray-600">{job.company}</p>
      {job.salary && <p className="text-green-600">Salary: {job.salary}</p>}
      {job.date && <p className="text-gray-500">Posted: {job.date}</p>}
      <p className="text-blue-500">Type: {job.type}</p>
      <span className={`inline-block px-2 py-1 rounded-full text-xs ${job.seen ? 'bg-gray-200 text-gray-700' : 'bg-green-200 text-green-700'}`}>
        {job.seen ? 'Seen' : 'New'}
      </span>
    </motion.div>
  );
};

export default JobCard;