import { useState } from 'react';
import './App.css';
import Footer from './components/Footer';
import Header from './components/Header';
import Input from './components/Input';
import Output from './components/Output';
import Send from './components/Send';

const App: React.FC = () => {
  const [profileImage, setProfileImage] = useState<File | null>(null);
  const [id, setId] = useState<number | null>(null);
  const [name, setName] = useState<string>('');

  return (
    <div className='flex flex-col min-h-screen'>
      <Header />
      <div className='flex items-center justify-between'>
        <div>
          <Input
            profileImage={profileImage}
            setProfileImage={setProfileImage}
          />
          <Send profileImage={profileImage} setId={setId} setName={setName} />
        </div>
        <Output id={id} name={name} />
      </div>
      <Footer />
    </div>
  );
};

export default App;
