export type FieldType = "int" | "string" | "list";

export interface FieldConfig {
  name: string;
  type: FieldType;
  placeholder?: string;
}

export interface EndpointConfig {
  key: string;
  label: string;
  endpoint: string | null;
  fields: FieldConfig[];
  isDynamic?: boolean;
  subtabs?: EndpointConfig[];
}

export const cancellable = ["binary", "devision", "wilson", "lucas"];

export const apiConfig: EndpointConfig[] = [
  {
    key: "gcd",
    label: "НОД",
    endpoint: null,
    fields: [],
    subtabs: [
      {
        key: "eea",
        label: "Расширенный",
        endpoint: "/api/eea",
        fields: [
          { name: "a", type: "string" },
          { name: "b", type: "string" },
        ],
      },
      {
        key: "gea",
        label: "Обобщённый",
        endpoint: "/api/gea",
        fields: [
          { name: "list", type: "list", placeholder: "15, -12, 18..." },
        ],
      },
    ],
  },
  {
    key: "pow",
    label: "Возведение в степень",
    endpoint: null,
    fields: [],
    subtabs: [
      {
        key: "binary",
        label: "Бинарный",
        endpoint: "/api/binpow",
        fields: [
          { name: "a", type: "string" },
          { name: "n", type: "string" },
          { name: "m", type: "string" },
        ],
      },
      {
        key: "crt",
        label: "CRT",
        endpoint: "/api/crtpow",
        fields: [
          { name: "a", type: "string" },
          { name: "n", type: "string" },
          { name: "m", type: "string" },
        ],
      },
    ],
  },
  {
    key: "inverse",
    label: "Обратный элемент",
    endpoint: "/api/inverse",
    fields: [
      { name: "a", type: "string" },
      { name: "m", type: "string" },
    ],
  },
  {
    key: "comparisons",
    label: "Сравнения",
    endpoint: null,
    fields: [],
    subtabs: [
      {
        key: "single",
        label: "Одно",
        endpoint: "/api/comparision/single",
        fields: [
          { name: "a", type: "string" },
          { name: "b", type: "string" },
          { name: "m", type: "string" },
        ],
      },
      {
        key: "system",
        label: "Система",
        endpoint: "/api/comparision/system",
        fields: [{ name: "coeffs", type: "list" }],
        isDynamic: true,
      },
      {
        key: "square",
        label: "Квадратичное",
        endpoint: "/api/comparision/square",
        fields: [
          { name: "a", type: "string" },
          { name: "b", type: "string" },
          { name: "m", type: "string" },
        ],
      },
    ],
  },
  {
    key: "jacobi",
    label: "Якоби",
    endpoint: "/api/jacobi",
    fields: [
      { name: "a", type: "string" },
      { name: "n", type: "string" },
    ],
  },
  {
    key: "primality",
    label: "Тесты простоты",
    endpoint: null,
    fields: [],
    subtabs: [
      {
        key: "devision",
        label: "Деление",
        endpoint: "/api/devision",
        fields: [{ name: "n", type: "string" }],
      },
      {
        key: "wilson",
        label: "Критерий Вильсона",
        endpoint: "/api/wilson",
        fields: [{ name: "n", type: "string" }],
      },
      {
        key: "lucas",
        label: "Люка",
        endpoint: "/api/lucas",
        fields: [{ name: "n", type: "string" }],
      },
      {
        key: "strassen",
        label: "Соловея-Штрассена",
        endpoint: "/api/strassen",
        fields: [
          { name: "n", type: "string" },
          { name: "k", type: "int" },
        ],
      },
      {
        key: "ferm",
        label: "Ферма",
        endpoint: "/api/ferm",
        fields: [
          { name: "n", type: "string" },
          { name: "k", type: "int" },
        ],
      },
      {
        key: "rabin",
        label: "Рабина-Миллера",
        endpoint: "/api/rabin",
        fields: [
          { name: "n", type: "string" },
          { name: "k", type: "int" },
        ],
      },
    ],
  },
];