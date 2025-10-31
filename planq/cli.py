from __future__ import annotations
import argparse
from datetime import date
from typing import Optional
from .storage import Storage
from .models import Task, Prio

PRIOS: tuple[Prio, ...] = ("low", "med", "high")

def parse_date(val: Optional[str]) -> Optional[date]:
    if val is None:
        return None
    if val == "":
        return None
    return date.fromisoformat(val)

def format_task(t: Task) -> str:
    status = "✔" if t.done else "✗"
    due = f" due:{t.due.isoformat()}" if t.due else ""
    return f"[{t.id:>3}] {status} {t.title} (prio:{t.prio}{due})"

def cmd_add(args: argparse.Namespace) -> None:
    st = Storage()
    tasks = st.all()
    new = Task(
        id=st.next_id(),
        title=args.title,
        prio=args.prio,
        due=parse_date(args.due),
    )
    tasks.append(new)
    st.save_all(tasks)
    print(f"Добавлена задача {new.id}: {new.title}")

def cmd_list(args: argparse.Namespace) -> None:
    st = Storage()
    tasks = st.all()
    if args.status == "todo":
        tasks = [t for t in tasks if not t.done]
    elif args.status == "done":
        tasks = [t for t in tasks if t.done]
    if args.prio:
        tasks = [t for t in tasks if t.prio == args.prio]
    if args.overdue:
        today = date.today()
        tasks = [t for t in tasks if (t.due and t.due < today and not t.done)]
    if not tasks:
        print("Задач не найдено.")
        return
    for t in sorted(tasks, key=lambda x: (x.done, x.prio != "high", x.prio != "med", x.due or date.max)):
        print(format_task(t))

def _get_by_id(tasks: list[Task], task_id: int) -> Task:
    for t in tasks:
        if t.id == task_id:
            return t
    raise SystemExit(f"Задача с id={task_id} не найдена")

def cmd_done(args: argparse.Namespace) -> None:
    st = Storage()
    tasks = st.all()
    t = _get_by_id(tasks, args.id)
    t.done = True
    st.save_all(tasks)
    print(f"Готово: {t.id} — {t.title}")

def cmd_remove(args: argparse.Namespace) -> None:
    st = Storage()
    tasks = st.all()
    before = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == before:
        raise SystemExit(f"Задача с id={args.id} не найдена")
    st.save_all(tasks)
    print(f"Удалена задача {args.id}")

def cmd_edit(args: argparse.Namespace) -> None:
    st = Storage()
    tasks = st.all()
    t = _get_by_id(tasks, args.id)
    if args.title is not None:
        t.title = args.title
    if args.prio is not None:
        t.prio = args.prio
    if args.due is not None:
        t.due = parse_date(args.due)
    st.save_all(tasks)
    print(f"Обновлено: {format_task(t)}")

def cmd_clear(args: argparse.Namespace) -> None:
    st = Storage()
    tasks = st.all()
    if args.done:
        tasks = [t for t in tasks if not t.done]
        msg = "Удалены выполненные задачи."
    else:
        tasks = []
        msg = "Список задач очищен."
    st.save_all(tasks)
    print(msg)

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="planq", description="Простой CLI‑планировщик задач")
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("add", help="Добавить задачу")
    pa.add_argument("title", help="Название задачи")
    pa.add_argument("--prio", choices=PRIOS, default="med")
    pa.add_argument("--due", help="Срок YYYY-MM-DD")
    pa.set_defaults(func=cmd_add)

    pl = sub.add_parser("list", help="Показать задачи")
    pl.add_argument("--status", choices=["all", "todo", "done"], default="all")
    pl.add_argument("--prio", choices=PRIOS)
    pl.add_argument("--overdue", action="store_true", help="Только просроченные")
    pl.set_defaults(func=cmd_list)

    pd = sub.add_parser("done", help="Отметить выполненной")
    pd.add_argument("id", type=int)
    pd.set_defaults(func=cmd_done)

    pr = sub.add_parser("remove", help="Удалить задачу по ID")
    pr.add_argument("id", type=int)
    pr.set_defaults(func=cmd_remove)

    pe = sub.add_parser("edit", help="Редактировать задачу")
    pe.add_argument("id", type=int)
    pe.add_argument("--title")
    pe.add_argument("--prio", choices=PRIOS)
    pe.add_argument("--due", help="Новый срок YYYY-MM-DD; пустая строка — удалить", nargs="?")
    pe.set_defaults(func=cmd_edit)

    pc = sub.add_parser("clear", help="Очистить список")
    grp = pc.add_mutually_exclusive_group()
    grp.add_argument("--done", action="store_true", help="Удалить только выполненные")
    grp.add_argument("--all", action="store_true", help="Удалить все")
    pc.set_defaults(func=cmd_clear)

    return p

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
