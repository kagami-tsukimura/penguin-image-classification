import axios from 'axios';

interface InputProps {
  profileImage: string;
  setData: React.Dispatch<React.SetStateAction<string>>;
}

const Send: React.FC<InputProps> = ({ profileImage, setData }) => {
  const url: string = 'http://127.0.0.1:8000/classify/';

  const predictImage = async () => {
    const formData = new FormData();
    formData.append('file', profileImage);
    axios
      .post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((res) => {
        setData(res.data.result);
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
