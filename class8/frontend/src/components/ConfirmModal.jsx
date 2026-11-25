import { AlertTriangle } from "lucide-react";
import { Button, Modal } from "./ui";

export default function ConfirmModal({ open, title, message, confirmLabel = "Confirm", loading, onConfirm, onClose }) {
  return (
    <Modal
      open={open}
      onClose={onClose}
      size="sm"
      title={title}
      footer={
        <>
          <Button variant="secondary" onClick={onClose}>
            Keep it
          </Button>
          <Button variant="danger" loading={loading} onClick={onConfirm}>
            {confirmLabel}
          </Button>
        </>
      }
    >
      <div className="flex gap-4">
        <div className="grid size-10 shrink-0 place-items-center rounded-full bg-rose-50 text-rose-600">
          <AlertTriangle className="size-5" />
        </div>
        <p className="text-sm text-slate-600">{message}</p>
      </div>
    </Modal>
  );
}
