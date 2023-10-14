import { useRef, useState } from 'react';
import { GiPenguin } from 'react-icons/gi';

interface InputProps {
  profileImage: File | null;
  setProfileImage: React.Dispatch<React.SetStateAction<File | null>>;
}

const Input: React.FC<InputProps> = ({ profileImage, setProfileImage }) => {
  const [isTooltip, setIsTooltip] = useState<boolean>(false);
  const inputRef = useRef<HTMLInputElement>(null!);

  const onProfileButtonClick = () => {
    inputRef.current.click();
  };

  const onFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const fileObject = e.target.files[0];
    setProfileImage(fileObject);
  };

  const resetFileInput = () => {
    inputRef.current && (inputRef.current.value = '');
    setProfileImage(null);
  };

  return (
    <div className='flex flex-col mt-8'>
      <div className='flex items-center justify-center'>
        {profileImage ? (
          <img
            src={URL.createObjectURL(profileImage)}
            className='object-contain h-64 w-64 '
            alt='プレビュー'
          />
        ) : (
          <></>
        )}
      </div>
      <input
        hidden
        ref={inputRef}
        type='file'
        accept='image/*'
        onChange={onFileInputChange}
      />
      <div className='flex justify-between'>
        {profileImage && (
          <button className='newtralButton' onClick={resetFileInput}>
            リセット
          </button>
        )}
        <button
          className='changeButton'
          onClick={onProfileButtonClick}
          onMouseMove={() => setIsTooltip(true)}
          onMouseLeave={() => setIsTooltip(false)}
        >
          {profileImage ? '画像を変更' : '画像を選択'}
        </button>
      </div>
      {!profileImage && isTooltip && (
        <div className='absolute mt-16 text-gray-400 rounded text-xs flex items-center'>
          <GiPenguin />
          HINT: お気に入りのペンギンを選択してね
          <GiPenguin className='transform scale-x-[-1]' />
        </div>
      )}
    </div>
  );
};

export default Input;
