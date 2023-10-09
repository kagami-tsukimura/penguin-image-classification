import axios from 'axios';
import { useEffect, useState } from 'react';
import { BallTriangle } from 'react-loader-spinner';

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
      .get(devUrl)
      .then(() => setUrl(`${devUrl}classify/`))
      .catch(() => setUrl(`${prodUrl}classify/`));
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
      <div className='mt-8'>
        {profileImage ? (
          <button className='sendButton' onClick={predictImage}>
            分類する 💭
          </button>
        ) : (
          <></>
        )}
        {isLoading ? (
          <div className='mt-8  text-sky-300 text-lg fixed top-1/4 left-2/3 -translate-x-1/2 -translate-y-1/2'>
            <BallTriangle
              height={100}
              width={100}
              radius={5}
              color='#4da9a8'
              ariaLabel='ball-triangle-loading'
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
