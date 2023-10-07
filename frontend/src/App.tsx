import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Footer from './components/Footer';
import Header from './components/Header';
import NotFound from './pages/404';
import Predict from './pages/Predict';

export const Router: React.FC = React.memo(() => {
  return (
    <BrowserRouter>
      <div className='flex flex-col min-h-screen'>
        <Header />
        <Routes>
          <Route path='/' element={<Predict />} />
          <Route path='*' element={<NotFound />} />
        </Routes>
        <Footer />
      </div>
    </BrowserRouter>
  );
});

export default Router;
