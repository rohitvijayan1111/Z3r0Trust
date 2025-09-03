"use client";
import { TextGenerateEffect } from "../ui/text-generate-effect";

const words = ` In a world of evolving threats, trust nothing by default and verify everything continuously to stay secure :)
`;

export function TextGenerateEffectDemo() {
  return <TextGenerateEffect words={words} />;
}
