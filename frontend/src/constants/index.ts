export interface Topic {
  id: number;
  name: string;
  image: string;
  desc: string[];
  tips: string;
  facility: string;
}

export const topic: Topic[] = [
  {
    id: 0,
    name: 'コウテイペンギン属',
    image:
      'https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/83259ef4-5c4c-c137-6802-11eca89f1288.jpeg',
    desc: ['コウテイペンギン', 'キングペンギン'],
    tips: 'アプテノディテス (Aptenodytes) 「翼のない潜水者」',
    facility: '名古屋港水族館など',
  },
  {
    id: 1,
    name: 'アデリーペンギン属',
    image:
      'https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/1ded7855-ee42-8b56-51d2-8cefb306e70b.jpeg',
    desc: ['アデリーペンギン', 'ジェンツーペンギン', 'ヒゲペンギン'],
    tips: 'ピゴスケリス (pygoscelis) 「尻についた肢（あし）」',
    facility: '名古屋港水族館など',
  },
  {
    id: 2,
    name: 'フンボルトペンギン属',
    image:
      'https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/0107977d-c2b8-99f4-0dfa-96131d7b7dda.jpeg',
    desc: ['フンボルトペンギン', 'ケープペンギン', 'マゼランペンギン'],
    tips: 'スフィニスクス (Spheniscus) 「楔のような」',
    facility: '東山動物園など',
  },
  {
    id: 3,
    name: 'マカロニペンギン属',
    image:
      'https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/a40a15e8-60ce-b572-82d6-142ff72aa327.jpeg',
    desc: ['マカロニペンギン', 'ロイヤルペンギン', 'イワトビペンギン'],
    tips: 'エウディプテス (Eudyptes) 「優れた潜水者」',
    facility: '新江ノ島水族館など',
  },
  {
    id: 4,
    name: 'キンメペンギン属',
    image:
      'https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/7d2c7fad-e847-90a2-b1a6-29a9d1bd48c9.jpeg',
    desc: ['キンメペンギン'],
    tips: 'メガディプテス (Megadyptes) 「大型の潜水者」',
    facility: '日本では飼育されていません...',
  },
  {
    id: 5,
    name: 'コガタペンギン属',
    image:
      'https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/b4b91171-7a03-c93a-6eed-1c7f1fd5809c.jpeg',
    desc: ['コガタペンギン', 'ハネジロペンギン'],
    tips: 'エウディプトゥラ (Eudyptula)「小さな潜水の名手」',
    facility: '長崎ペンギン水族館など',
  },
  {
    id: 6,
    name: 'その他',
    image:
      'https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3292052/60ac5d37-3f14-af42-6ef5-cf5be83ef531.jpeg',
    desc: ['ペンギン以外'],
    tips: 'ペンギンかペンギン以外か',
    facility: 'その他',
  },
];
