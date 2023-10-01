import axios from 'axios';

interface SendProps {
  profileImage: File | null; // File オブジェクトを受け取る
  setData: React.Dispatch<React.SetStateAction<string>>;
}

const Send: React.FC<SendProps> = ({ profileImage, setData }) => {
  const url: string = 'http://127.0.0.1:8000/classify/';

  const predictImage = async () => {
    if (!profileImage) return; // ファイルが選択されていない場合は処理しない

    const formData = new FormData();
    formData.append('file', profileImage); // File オブジェクトを追加
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
