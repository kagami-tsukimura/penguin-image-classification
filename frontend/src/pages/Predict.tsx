import React, { createContext, useState } from 'react';
import '../App.css';
import Gallery from '../components/Gallery';
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
        <div className='sm:flex sm:items-center sm:justify-between'>
          <div>
            <Input
              profileImage={profileImage}
              setProfileImage={setProfileImage}
            />
            <Send profileImage={profileImage} setId={setId} setName={setName} />
          </div>
          <Output id={id} name={name} />
        </div>
        <Gallery />
      </SendContext.Provider>
    </>
  );
};

export default Predict;
