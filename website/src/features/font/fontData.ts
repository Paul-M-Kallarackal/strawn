import characterSet from "@moriatz-labs/strawn/files/Strawn-Character-Set.json";
import variableFontUrl from "@moriatz-labs/strawn/files/Strawn-Variable.ttf?url";

export const fontFacts = {
  family: "Strawn",
  variableLabel: "Variable 100—700",
  version: "0.7.0",
  downloadUrl: variableFontUrl,
  repositoryUrl: "https://github.com/Paul-M-Kallarackal/strawn",
  defaultWeight: 500,
  characterCount: 319,
  metrics: [
    { label: "Cap height", value: 720 },
    { label: "X-height", value: 520 },
    { label: "Baseline", value: 0 },
    { label: "Descender", value: -220 },
  ],
} as const;

export const fontGlyphs = characterSet.characters
  .filter(({ name }) => !name.startsWith("COMBINING "))
  .map(({ character }) => character)
  .filter((character) => character.trim().length > 0);

export const fontCharacterList = characterSet.characters
  .map(({ character, name }) => name.startsWith("COMBINING ") ? `\u00a0${character}` : character)
  .join(" ");
