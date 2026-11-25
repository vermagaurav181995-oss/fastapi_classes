import { cx } from "../lib/utils";

const HUES = [222, 262, 12, 158, 199, 330, 36, 286, 174, 4, 240, 140];

export default function BookCover({ book, className, compact = false }) {
  const hue = HUES[(book.id ?? 0) % HUES.length];
  const style = {
    background: `linear-gradient(140deg, hsl(${hue} 65% 52%), hsl(${(hue + 35) % 360} 60% 30%))`,
  };

  return (
    <div className={cx("relative overflow-hidden rounded-xl text-white", className)} style={style}>
      <div className="absolute inset-y-0 left-0 w-2 bg-black/15" />
      <div className="absolute -right-8 -top-8 size-28 rounded-full bg-white/10" />
      <div className="absolute -bottom-10 left-6 size-32 rounded-full bg-black/10" />
      {!compact && (
        <div className="relative flex h-full flex-col justify-between p-5 pl-6">
          <span className="text-[10px] font-semibold uppercase tracking-[0.2em] text-white/70">{book.genre}</span>
          <div>
            <p className="font-display text-xl font-semibold leading-tight line-clamp-3 drop-shadow-sm">{book.title}</p>
            <p className="mt-2 text-xs text-white/80 line-clamp-1">{book.author}</p>
          </div>
        </div>
      )}
    </div>
  );
}
