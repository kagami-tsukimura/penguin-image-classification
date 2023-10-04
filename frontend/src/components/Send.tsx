import axios from 'axios';
import process from 'process';

interface SendProps {
  profileImage: File | null;
  setId: React.Dispatch<React.SetStateAction<number | null>>;
  setName: React.Dispatch<React.SetStateAction<string>>;
}

const Send: React.FC<SendProps> = ({ profileImage, setId, setName }) => {
  const ENV: string | undefined = process.env.ENV;
  let url: string = 'http://127.0.0.1:8000/classify/';
  if (ENV) {
    url = 'https://penguin-image-classification-api.onrender.com/';
  }

  const predictImage = async (): Promise<void> => {
    if (!profileImage) return;

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
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
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
    </div>
  );
};

export default Send;
