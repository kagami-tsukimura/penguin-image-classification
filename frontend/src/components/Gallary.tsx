import { useContext, useState } from 'react';
import { samples } from '../constants/gallary';
import { SendContext } from '../pages/Predict';

const Gallary = () => {
  const [isChangeSample, setIsChangeSample] = useState<boolean>(true);
  const { setImage } = useContext(SendContext);
  const [shuffledSamples, setShuffledSamples] = useState(samples.slice(0, 4));

  const fetchImage = async (imageUrl: string): Promise<File> => {
    const response = await fetch(imageUrl);
    const imageBlob = await response.blob();
    return new File([imageBlob], `${imageUrl}.jpg`, {
      type: 'image/jpeg',
    });
  };

  const shuffleArray = (array: any[]) => {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  };

  return (
    <div className='bg-white border-b rounded-lg border-gray-200 dark:bg-gray-700 dark:border-blue-500 py-4 sm:py-6 lg:py-8 my-4 sm:my-6 lg:my-8'>
      <div className='mx-auto max-w-screen-2xl px-4 md:px-8'>
        <div className='mb-6 md:mb-10'>
          <h2 className='mb-2 text-center text-2xl font-bold text-cyan-600 dark:text-cyan-200 md:mb-4 lg:text-3xl'>
            Samples
          </h2>
          <span className='text-center text-sm text-gray-700 dark:text-gray-400 lg:text-lg'>
            迷ったらサンプル画像をクリック！
          </span>
        </div>
        <div className='grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6 xl:gap-8'>
          {shuffledSamples.map((sample, id) => (
            <div
              className='group relative flex h-48 items-end justify-end overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-96'
              key={sample.id}
              onClick={async () => {
                const file = await fetchImage(sample.image);
                setImage(file);
              }}
            >
              <img
                src={sample.image}
                loading='lazy'
                alt={`sample-${sample.id}`}
                className='absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110 hover:cursor-pointer'
              />
              <div className='pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 via-transparent to-transparent opacity-50'></div>
              <span className='relative mr-3 mb-3 inline-block rounded-lg border border-gray-500 px-2 py-1 text-xs text-gray-200 backdrop-blur md:px-3 md:text-sm'>
                {id + 1}
              </span>
            </div>
          ))}
        </div>
        <div className='flex flex-col items-center mt-8'>
          <button
            className='changeButton mt-8'
            onClick={() => {
              setIsChangeSample(!isChangeSample);
              const newShuffledSamples = shuffleArray(samples).slice(0, 4);
              setShuffledSamples(newShuffledSamples);
            }}
          >
            他の画像に変更
          </button>
        </div>
      </div>
    </div>
  );
};

export default Gallary;
