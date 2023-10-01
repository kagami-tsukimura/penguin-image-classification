import axios from 'axios';

interface InputProps {
  profileImage: string;
  setData: React.Dispatch<React.SetStateAction<string>>;
}

const Send: React.FC<InputProps> = ({ profileImage, setData }) => {
  const url: string = 'http://127.0.0.1:8000/';
  const predictImage = () => {
    axios.get(url).then((res) => setData(res.data.message));
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
