// ไฟล์นี้เป็น Modal สำหรับจัดการข้อมูลประเภทเพศ
// ใช้สำหรับสร้าง (create), อัพเดท (update), หรือดูข้อมูล (read) โดยแสดงฟอร์มที่มีช่อง description
import React, { useState, useEffect } from "react";
import { Modal, Box, TextField, Typography, Stack } from "@mui/material";
import SaveButton from "../buttons/SaveButton";

// อินเทอร์เฟซกำหนดโครงสร้างข้อมูลสำหรับฟอร์ม
interface typeOfFormData {
  id: number | null; // รหัสประเภทเพศ (null สำหรับการสร้างใหม่)
  description: string; // คำอธิบายประเภทเพศ
}

// สไตล์สำหรับ Modal เพื่อให้แสดงตรงกลางหน้าจอ
const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400, // ความกว้างคงที่
  bgcolor: "background.paper", // พื้นหลังสีขาว
  boxShadow: 24, // เงาเพื่อความสวยงาม
  p: 4, // padding ภายใน
};

// อินเทอร์เฟซสำหรับ props ที่ component นี้รับ
interface typeofModalProps {
  open: boolean; // ควบคุมการเปิด/ปิด Modal
  onClose: () => void; // ฟังก์ชันเมื่อปิด Modal
  initialDetail: typeOfFormData; // ข้อมูลเริ่มต้นสำหรับฟอร์ม
  onSubmit: (updatedData: typeOfFormData) => void; // ฟังก์ชันเมื่อ submit ฟอร์ม
  openModalFor: string; // โหมดของ Modal ("create", "update", "read")
}

// Component หลักสำหรับแสดง Modal
export default function GenderTypeModal({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
}: typeofModalProps) {
  // State สำหรับเก็บข้อมูลฟอร์ม
  const [formData, setFormData] = useState<typeOfFormData>({
    id: null,
    description: "",
  });

  // useEffect สำหรับอัพเดท formData เมื่อ initialDetail เปลี่ยน
  useEffect(() => {
    console.log("form initial detail = ", initialDetail);
    setFormData(initialDetail);
  }, [initialDetail]);

  // ฟังก์ชันจัดการการเปลี่ยนแปลงของ TextField
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // ฟังก์ชันจัดการการ submit ฟอร์ม
  const handleSubmit = () => {
    // Validation เพื่อป้องกันข้อมูลไม่สมบูรณ์
    if (!formData.description) {
      alert("Description is required");
      return;
    }
    onSubmit(formData); // ส่งข้อมูลไปยัง parent
    onClose(); // ปิด Modal
  };

  // useEffect สำหรับ log โหมดของ Modal เพื่อ debug
  useEffect(() => {
    console.log("openModalFor = ", openModalFor);
  }, [openModalFor]);

  // JSX สำหรับ UI ของ Modal
  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography variant="h6" component="h2">
          Gender Type Details
        </Typography>
        <TextField
          label="Description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          fullWidth
          margin="normal"
          disabled={openModalFor === "read"} // ปิดการแก้ไขในโหมด read
          required
        />
        {/* ปุ่ม Save สำหรับโหมด create และ update */}
        {openModalFor !== "read" && (
          <Stack direction="row" justifyContent="flex-end" sx={{ mt: 2 }}>
            <SaveButton onClick={handleSubmit} />
          </Stack>
        )}
      </Box>
    </Modal>
  );
}