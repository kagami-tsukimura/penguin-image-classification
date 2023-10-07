const NotFound = () => {
  return (
    <div className='flex justify-center items-center h-screen'>
      <div>
        <img
          src='https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/ef709a3e-3e7b-0656-fed5-951cb21f9c53.jpeg'
          loading='lazy'
          alt='404 Not Found'
        />
        <div className='relative mx-auto flex h-96 w-full items-center justify-center overflow-hidden rounded-lg sm:w-96'>
          <a
            href='/'
            className='inline-block rounded-lg bg-gray-200 px-8 py-3 text-center text-sm font-semibold text-gray-500 outline-none ring-indigo-300 transition duration-100 hover:bg-gray-300 focus-visible:ring active:text-gray-700 md:text-base'
          >
            Go home
          </a>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
