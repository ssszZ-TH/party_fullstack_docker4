import React, { useState, useEffect } from "react";
import {
  Modal,
  Box,

  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
} from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateField } from "@mui/x-date-pickers/DateField";
import dayjs from "dayjs";
import SaveButton from "../buttons/SaveButton";

interface typeOfFormData {
  id: number | null;
  fromdate: string;
  thrudate: string;
  person_id: number;
  country_id: number;
}

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
};

interface typeOfDD {
  id: number;
  text: string;
}

interface typeofModalProps {
  open: boolean;
  onClose: () => void;
  initialDetail: typeOfFormData;
  onSubmit: (updatedCountry: typeOfFormData) => void;
  openModalFor: string;
  personDD: Array<typeOfDD>;
  countryDD: Array<typeOfDD>;
}

export default function Modal_citizenship({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
  personDD,
  countryDD,
}: typeofModalProps) {
  const [formData, setFormData] = useState<typeOfFormData>({
    id: null,
    fromdate: "",
    thrudate: "",
    country_id: 0,
    person_id: 0,
  });

  // ใช้ useEffect เพื่ออัปเดต formData เมื่อ initialDetail เปลี่ยน
  useEffect(() => {
    console.log("form initial detail = ", initialDetail);
    setFormData(initialDetail);
  }, [initialDetail]);

  const handleDateChange = (name: string, value: dayjs.Dayjs | null) => {
    // แปลงค่าเป็นรูปแบบ YYYY-MM-DD หรือค่าว่างถ้าไม่มีค่า
    const dateValue = value ? value.format("YYYY-MM-DD") : "";
    setFormData({ ...formData, [name]: dateValue });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = () => {
    onSubmit(formData);
    onClose();
  };

  useEffect(() => {
    console.log("openModalFor = ", openModalFor);
  }, [openModalFor]);

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography variant="h6" component="h2">
          Details
        </Typography>

        <LocalizationProvider dateAdapter={AdapterDayjs}>
          {/* From Date Field */}
          <DateField
            label="From Date"
            value={formData.fromdate ? dayjs(formData.fromdate) : null}
            onChange={(newValue) => handleDateChange("fromdate", newValue)}
            format="YYYY-MM-DD"
            fullWidth
            margin="normal"
            sx={{ mb: 2 }}
          />

          {/* Thru Date Field */}
          <DateField
            label="Thru Date"
            value={formData.thrudate ? dayjs(formData.thrudate) : null}
            onChange={(newValue) => handleDateChange("thrudate", newValue)}
            format="YYYY-MM-DD"
            fullWidth
            margin="normal"
            sx={{ mb: 2 }}
          />
        </LocalizationProvider>

        <FormControl fullWidth margin="normal">
          <InputLabel id="person-select-label">Person</InputLabel>
          <Select
            labelId="person-select-label"
            name="person_id"
            value={formData.person_id ?? ""}
            onChange={handleChange}
          >
            {personDD.map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.text}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal">
          <InputLabel id="country-select-label">Country</InputLabel>
          <Select
            labelId="country-select-label"
            name="country_id"
            value={formData.country_id ?? ""}
            onChange={handleChange}
          >
            {countryDD.map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.text}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* ใช้ Stack เพื่อจัดตำแหน่งปุ่ม */}
        <Stack direction="row" justifyContent="flex-end" sx={{ mt: 2 }}>
          <SaveButton onClick={handleSubmit} />
        </Stack>
      </Box>
    </Modal>
  );
}
