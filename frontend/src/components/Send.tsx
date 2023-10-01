interface InputProps {
  profileImage: string;
}

const Send: React.FC<InputProps> = ({ profileImage }) => {
  return (
    <div className='mt-8'>
      {profileImage ? (
        <button className='button outline-sky-700  text-sky-700 hover:bg-sky-700 hover:text-white'>
          分類する
        </button>
      ) : (
        <></>
      )}
    </div>
  );
};

export default Send;
