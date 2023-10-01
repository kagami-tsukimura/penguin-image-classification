interface ApiData {
  data: string;
}

const Output: React.FC<ApiData> = ({ data }) => {
  return <div>{data}</div>;
};

export default Output;
