import React, { createContext, useState } from 'react';
import '../App.css';
import Gallary from '../components/Gallary';
import Input from '../components/Input';
import Output from '../components/Output';
import Send from '../components/Send';

export const SendContext = createContext<{
  setImage: (file: File) => void;
}>({
  setImage: () => {},
});

const Predict: React.FC = () => {
  const [profileImage, setProfileImage] = useState<File | null>(null);
  const [id, setId] = useState<number | null>(null);
  const [name, setName] = useState<string>('');

  return (
    <>
      <SendContext.Provider
        value={{ setImage: (file) => setProfileImage(file) }}
      >
        <div className='flex items-start justify-between'>
          <div>
            <Input
              profileImage={profileImage}
              setProfileImage={setProfileImage}
            />
            <Send profileImage={profileImage} setId={setId} setName={setName} />
          </div>
          <Output id={id} name={name} />
        </div>
        <Gallary />
      </SendContext.Provider>
    </>
  );
};

export default Predict;
