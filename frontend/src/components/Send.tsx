import axios from 'axios';
import { useEffect, useState } from 'react';
import { RotatingLines } from 'react-loader-spinner';

interface SendProps {
  profileImage: File | null;
  setId: React.Dispatch<React.SetStateAction<number | null>>;
  setName: React.Dispatch<React.SetStateAction<string>>;
}

const Send: React.FC<SendProps> = ({ profileImage, setId, setName }) => {
  const [url, setUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  useEffect(() => {
    const devUrl: string = 'http://127.0.0.1:8000/';
    const prodUrl: string = 'https://penguin-image-classification-api.fly.dev/';
    axios
      .get(prodUrl)
      .then(() => setUrl(`${prodUrl}classify/`))
      .catch(() => setUrl(`${devUrl}classify/`));
  }, []);

  const predictImage = async (): Promise<void> => {
    if (!profileImage) return;
    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', profileImage);
    axios
      .post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((res) => {
        setId(Number(res.data.id));
        setName(res.data.name);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
      });
  };

  return (
    <>
      <div className='flex justify-center mt-8'>
        {profileImage ? (
          <button className='sendButton' onClick={predictImage}>
            分類する 💭
          </button>
        ) : (
          <></>
        )}
        {isLoading ? (
          <div className='absolute mt-5 ml-52'>
            <RotatingLines
              strokeColor='grey'
              strokeWidth='5'
              animationDuration='0.75'
              width='42'
              visible={true}
            />
          </div>
        ) : (
          <></>
        )}
      </div>
    </>
  );
};

export default Send;
