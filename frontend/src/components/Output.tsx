import { Topic, topic } from '../constants';

interface ApiData {
  id: number | null;
  name: string;
}

const Output: React.FC<ApiData> = ({ id, name }) => {
  const getTopicById = (id: number | null): Topic | undefined =>
    topic.find((item) => item.id === id);

  const topicById = getTopicById(id);

  return (
    <>
      {topicById ? (
        <div className='text-start mt-8'>
          <div className='flex flex-col bg-white border shadow-sm rounded-xl dark:bg-gray-800 dark:border-gray-700 dark:shadow-slate-700/[.7]'>
            <img
              className='object-contain h-64 w-64 mx-auto'
              src={topicById.image}
              alt='Image Description'
            ></img>
            <div className='p-4 md:p-5'>
              <h3 className='text-lg font-bold text-gray-800 dark:text-white'>
                分類結果: {name}
              </h3>
              <p className='mt-1 text-gray-800 dark:text-gray-400'>
                種族:
                {topicById.desc.map((desc, i) =>
                  i === 0 ? (
                    <span key={i} className='ml-1'>
                      {desc}
                    </span>
                  ) : (
                    <p key={i} className='ml-10'>
                      {desc}
                    </p>
                  )
                )}
                <br />
                TIPS: {topicById.tips}
                <br />
                {name}に会える水族館: {topicById.facility}
              </p>
            </div>
          </div>
        </div>
      ) : (
        ''
      )}
    </>
  );
};

export default Output;
