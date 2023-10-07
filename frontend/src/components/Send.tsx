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
          <button
            className='button outline-sky-700  text-sky-700 hover:bg-sky-700 hover:text-white'
            onClick={predictImage}
          >
            分類する
          </button>
        ) : (
          <></>
        )}
        {isLoading ? (
          <div className='mt-8  text-sky-300 text-lg'>
            <BallTriangle
              height={100}
              width={100}
              radius={5}
              color='#4da9a8'
              ariaLabel='ball-triangle-loading'
              visible={true}
              wrapperStyle={{
                transform: '(0, 0)',
                display: 'block',
                position: 'absolute',
                top: `calc(50% - ${100 / 2}px)`,
                left: `calc(50% - ${100 / 2}px)`,
              }}
            />
            <span>ペンギン分類中...</span>
          </div>
        ) : (
          <></>
        )}
      </div>
    </>
  );
};

export default Send;
