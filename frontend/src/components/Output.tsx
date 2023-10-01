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
      <div>
        分類結果: {name}
        <br />
        {topicById ? (
          <>
            種族: {topicById.desc}
            <br />
            TIPS: {topicById.tips}
            <br />
            {name}に会える水族館: {topicById.facility}
          </>
        ) : (
          '該当するトピックが見つかりません'
        )}
      </div>
    </>
  );
};

export default Output;
