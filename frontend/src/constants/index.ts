export interface Topic {
  id: number;
  name: string;
  desc: string;
  tips: string;
  facility: string;
}

export const topic: Topic[] = [
  {
    id: 0,
    name: 'コウテイペンギン属',
    desc: 'コウテイペンギン or キングペンギン',
    tips: 'アプテノディテス (Aptenodytes) は「翼のない潜水者」',
    facility: '名古屋港水族館など',
  },
  {
    id: 1,
    name: 'アデリーペンギン属',
    desc: 'アデリーペンギン or ジェンツーペンギン or ヒゲペンギン',
    tips: 'ピゴスケリス (pygoscelis) は「尻についた肢（あし）」',
    facility: '名古屋港水族館など',
  },
  {
    id: 2,
    name: 'フンボルトペンギン属',
    desc: 'ガラパゴスペンギン or ケープペンギン or フンボルトペンギン or マゼランペンギン',
    tips: 'スフィニスクス (Spheniscus) は「楔のような」',
    facility: '東山動物園など',
  },
  {
    id: 3,
    name: 'マカロニペンギン属',
    desc: 'フィヨルドランドペンギン or シュレーターペンギン or スネアーズペンギン or マカロニペンギン or ロイヤルペンギン or イワトビペンギン',
    tips: 'エウディプテス (Eudyptes) は「優れた潜水者」',
    facility: '新江ノ島水族館など',
  },
  {
    id: 4,
    name: 'キンメペンギン属',
    desc: 'キンメペンギン',
    tips: 'メガディプテス (Megadyptes) は「大型の潜水者」',
    facility: '日本では飼育されていません...',
  },
  {
    id: 5,
    name: 'コガタペンギン属',
    desc: 'コガタペンギン or ハネジロペンギン',
    tips: 'エウディプトゥラ (Eudyptula)は「非常に小さい」「優れた潜水者」',
    facility: '長崎ペンギン水族館など',
  },
  {
    id: 6,
    name: 'その他',
    desc: 'ペンギン以外',
    tips: 'ペンギンかペンギン以外か',
    facility: 'その他',
  },
];
