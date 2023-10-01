import { useState } from 'react';
import './App.css';
import Footer from './components/Footer';
import Header from './components/Header';
import Input from './components/Input';
import Output from './components/Output';
import Send from './components/Send';

const App: React.FC = () => {
  const [profileImage, setProfileImage] = useState<string>('');
  const [data, setData] = useState<string>('');

  return (
    <>
      <Header />
      <div className='flex items-center justify-between'>
        <div>
          <Input
            profileImage={profileImage}
            setProfileImage={setProfileImage}
          />
          <Send profileImage={profileImage} setData={setData} />
        </div>

        <Output data={data} />
      </div>
      <Footer />
    </>
  );
};

export default App;
