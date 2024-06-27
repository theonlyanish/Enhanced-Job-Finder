'use client';

import SearchForm from '../components/SearchForm';
import JobList from '../components/JobList';

export default function Home() {
  return (
    <>
      <SearchForm />
      <JobList />
    </>
  );
}