import React, { useState } from 'react';
import '../App.css';
import Input from '../components/Input';
import Output from '../components/Output';
import Send from '../components/Send';

const Predict: React.FC = () => {
  const [profileImage, setProfileImage] = useState<File | null>(null);
  const [id, setId] = useState<number | null>(null);
  const [name, setName] = useState<string>('');

  return (
    <>
      <div>
        <Input profileImage={profileImage} setProfileImage={setProfileImage} />
        <Send profileImage={profileImage} setId={setId} setName={setName} />
      </div>
      <Output id={id} name={name} />
    </>
  );
};

export default Predict;
