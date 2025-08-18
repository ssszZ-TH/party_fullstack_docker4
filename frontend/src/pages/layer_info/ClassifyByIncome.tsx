// ไฟล์นี้เป็นหน้า ClassifyByIncome สำหรับแสดงตารางข้อมูลการจำแนกตามช่วงรายได้
// รองรับการแสดงข้อมูล (read), สร้าง (create), อัพเดท (update), และลบ (delete)
// ใช้ DataTable จาก MUI สำหรับแสดงข้อมูล และ Modal สำหรับฟอร์ม
import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal_classifybyincome from "../../components/Modal/Modal_ClassifyByIncome"; // Modal สำหรับจัดการฟอร์ม
import Loading from "../../components/Loading";
import {
  create,
  get,
  list,
  update,
  deleteById,
} from "../../services/classifybyincome"; // Service สำหรับ API classifybyincome
import { list as listPartyType } from "../../services/partytype"; // Service สำหรับ dropdown PartyType
import { list as listPerson } from "../../services/person"; // Service สำหรับ dropdown Person
import { list as listIncomeRange } from "../../services/incomerange"; // Service สำหรับ dropdown IncomeRange
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

// Component หลักสำหรับหน้า ClassifyByIncome
export default function ClassifyByIncome() {
  // กำหนดคอลัมน์สำหรับ DataTable
  // รวม description จากตาราง incomerange เพื่อแสดงผล
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 }, // คอลัมน์แสดงรหัส
    {
      field: "fromdate",
      headerName: "From Date YYYY-MM-DD",
      width: 150, // คอลัมน์วันที่เริ่มต้น
    },
    {
      field: "thrudate",
      headerName: "Thru Date YYYY-MM-DD",
      width: 150, // คอลัมน์วันที่สิ้นสุด
    },
    {
      field: "party_id",
      headerName: "Party ID",
      width: 100, // คอลัมน์รหัส Party (จาก Person)
    },
    // {
    //   field: "party",
    //   headerName: "Person Details",
    //   width: 200,
    //   renderCell: (params) => {
    //     // แสดงข้อมูล Person จาก personDD โดยค้นหาด้วย party_id
    //     const obj = personDD.find((item) => item.id === params.row.party_id);
    //     return <>{obj ? obj.text : "N/A"}</>;
    //   },
    // },
    // {
    //   field: "party_type_id",
    //   headerName: "Party Type ID",
    //   width: 100, // คอลัมน์รหัสประเภท Party
    // },
    // {
    //   field: "party_type",
    //   headerName: "Party Type",
    //   width: 200,
    //   renderCell: (params) => {
    //     // แสดงข้อมูล PartyType จาก partyTypeDD
    //     const item = partyTypeDD.find((c) => c.id === params.row.party_type_id);
    //     return <>{item ? item.text : "N/A"}</>;
    //   },
    // },
    {
      field: "income_range_id",
      headerName: "Income Range ID",
      width: 100, // คอลัมน์รหัสช่วงรายได้
    },
    // {
    //   field: "description",
    //   headerName: "Income Range Description",
    //   width: 200, // คอลัมน์คำอธิบายช่วงรายได้ (จาก incomerange)
    // },
    // {
    //   field: "update",
    //   headerName: "",
    //   width: 100,
    //   renderCell: (params) => (
    //     // ปุ่ม Update เรียก handleUpdateButton
    //     <UpdateButton onClick={() => handleUpdateButton(params.row)} />
    //   ),
    // },
    // {
    //   field: "delete",
    //   headerName: "",
    //   width: 100,
    //   renderCell: (params) => (
    //     // ปุ่ม Delete เรียก handleDeleteButton
    //     <DeleteButton onClick={() => handleDeleteButton(params.row.id)} />
    //   ),
    // },
  ];

  // State สำหรับเก็บข้อมูลตาราง
  const [rows, setRows] = useState([]);
  // State สำหรับควบคุมสถานะการโหลด
  const [loading, setLoading] = useState(true);
  // State สำหรับควบคุมการเปิด/ปิด Modal
  const [open, setOpen] = useState(false);
  // State สำหรับเก็บข้อมูลเริ่มต้นของฟอร์มใน Modal
  const [initialDetail, setInitialDetail] = useState<typeofTableRow>({
    id: null,
    fromdate: "",
    thrudate: "",
    party_id: "",
    party_type_id: "",
    income_range_id: "",
  });

  // อินเทอร์เฟซสำหรับข้อมูลใน dropdown
  interface typeOfDD {
    id: number;
    text: string;
  }

  // ค่าเริ่มต้นสำหรับ dropdown ถ้า API ยังไม่โหลด
  const defaultPersonDD = [{ id: 0, text: "" }];
  const defaultPartyTypeDD = [{ id: 0, text: "" }];
  const defaultIncomeRangeDD = [{ id: 0, text: "" }];

  // State สำหรับเก็บข้อมูล dropdown
  const [personDD, setPersonDD] = useState<typeOfDD[]>(defaultPersonDD);
  const [partyTypeDD, setPartyTypeDD] = useState<typeOfDD[]>(defaultPartyTypeDD);
  const [incomeRangeDD, setIncomeRangeDD] = useState<typeOfDD[]>(defaultIncomeRangeDD);

  // State สำหรับเก็บโหมดของ Modal (create, update, read)
  const [openModalFor, setOpenModalFor] = useState("");

  // อินเทอร์เฟซสำหรับแถวในตารางและฟอร์ม
  // ไม่รวม description เพราะใช้ในตารางเท่านั้น
  interface typeofTableRow {
    id: number | null;
    fromdate: string;
    thrudate: string;
    party_id: number ;
    party_type_id: number;
    income_range_id: number;
    description?: string; // Optional สำหรับแสดงในตาราง
  }

  // ฟังก์ชันจัดการเมื่อกดปุ่ม Update
  const handleUpdateButton = async (row: typeofTableRow) => {
    console.log("edit button receive value = ", row);
    setInitialDetail({
      id: row.id,
      fromdate: row.fromdate,
      thrudate: row.thrudate,
      party_id: row.party_id,
      party_type_id: row.party_type_id,
      income_range_id: row.income_range_id,
    }); // ตั้งค่า initialDetail (ไม่รวม description)
    openModal("update"); // เปิด Modal ในโหมด update
  };

  // ฟังก์ชันจัดการเมื่อกดปุ่ม Delete
  const handleDeleteButton = async (id: number) => {
    console.log("delete button receive value = ", id);
    setLoading(true);
    await deleteById({ id }); // เรียก API ลบข้อมูล
    await fetchDataTable(); // รีเฟรชตาราง
    setLoading(false);
  };

  // ฟังก์ชันดึงข้อมูลตารางจาก API
  const fetchDataTable = async () => {
    setLoading(true);
    const res = await list(); // เรียก API `/v1/classifybyincome`
    setRows(res); // อัพเดทข้อมูลตาราง
    setLoading(false);
  };

  // อินเทอร์เฟซสำหรับข้อมูล Person จาก API
  interface TypeOfPerson {
    id: number; // อ้างอิง party_id
    socialsecuritynumber: string;
    birthdate: string;
    mothermaidenname: string | null;
    totalyearworkexperience: number;
    comment: string;
  }

  // อินเทอร์เฟซสำหรับข้อมูล PartyType จาก API
  interface TypeOfPartyType {
    id: number;
    description: string;
  }

  // อินเทอร์เฟซสำหรับข้อมูล IncomeRange จาก API
  interface TypeOfIncomeRange {
    id: number;
    description: string;
  }

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ Person
  // Person.id อ้างอิง party_id ใน classifybyincome
  const fetchPersonDD = async () => {
    const res: Array<TypeOfPerson> = await listPerson();
    const DD = res.map((item) => ({
      id: item.id,
      text: `${item.socialsecuritynumber} ${item.comment || "N/A"}`,
    }));
    setPersonDD(DD);
  };

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ PartyType
  const fetchPartyTypeDD = async () => {
    const res: Array<TypeOfPartyType> = await listPartyType();
    const DD = res.map((item) => ({
      id: item.id,
      text: item.description || "N/A",
    }));
    setPartyTypeDD(DD);
  };

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ IncomeRange
  const fetchIncomeRangeDD = async () => {
    const res: Array<TypeOfIncomeRange> = await listIncomeRange();
    const DD = res.map((item) => ({
      id: item.id,
      text: item.description || "N/A",
    }));
    setIncomeRangeDD(DD);
  };

  // useEffect สำหรับโหลดข้อมูลเมื่อ component เริ่มทำงาน
  useEffect(() => {
    fetchPersonDD(); // โหลด dropdown Person
    fetchPartyTypeDD(); // โหลด dropdown PartyType
    fetchIncomeRangeDD(); // โหลด dropdown IncomeRange
    fetchDataTable(); // โหลดข้อมูลตาราง
  }, []);

  // ฟังก์ชันเปิด Modal
  const openModal = (reason?: string) => {
    setOpenModalFor(reason || ""); // ตั้งค่าโหมด (create, update, read)
    setOpen(true); // เปิด Modal
  };

  // ฟังก์ชันปิด Modal
  const closeModal = () => {
    setOpen(false); // ปิด Modal
    // รีเซ็ต initialDetail เพื่อเคลียร์ฟอร์ม
    setInitialDetail({
      id: null,
      fromdate: "",
      thrudate: "",
      party_id: 0,
      party_type_id: 0,
      income_range_id: 0,
    });
    setOpenModalFor("");
  };

  // ฟังก์ชันจัดการการ submit ฟอร์มจาก Modal
  const handleSubmit = async (payload: typeofTableRow) => {
    setLoading(true);
    try {
      if (payload.id) {
        // โหมด Update
        await update({
          id: payload.id,
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          party_id: payload.party_id,
          party_type_id: payload.party_type_id,
          income_range_id: payload.income_range_id,
        });
        console.log("Updated with payload:", payload);
      } else {
        // โหมด Create
        await create({
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          party_id: payload.party_id,
          party_type_id: payload.party_type_id,
          income_range_id: payload.income_range_id,
        });
        console.log("Created with payload:", payload);
      }
    } catch (error) {
      console.error("while submit catch error = ", error); // Log error เพื่อ debug
    } finally {
      await fetchDataTable(); // รีเฟรชตาราง
      closeModal(); // ปิด Modal
      setLoading(false);
    }
  };

  // JSX สำหรับ UI ของหน้า
  return (
    <>
      <AppBarCustom title="Classify By Income การจำแนกตามช่วงรายได้" /> {/* แถบด้านบน */}
      {loading ? (
        <Loading /> // แสดง Loading component ถ้ากำลังโหลด
      ) : (
        <DataTable
          columns={columns}
          rows={rows}
          getRowId={(row) => row.id} // ใช้ id เป็น key
        />
      )}
      {/* <AddButton
        onClick={() => {
          openModal("create"); // เปิด Modal ในโหมด create
        }}
      /> */}
      <Modal_classifybyincome
        open={open}
        onClose={closeModal}
        initialDetail={initialDetail}
        onSubmit={handleSubmit}
        openModalFor={openModalFor}
        personDD={personDD}
        partyTypeDD={partyTypeDD}
        incomeRangeDD={incomeRangeDD}
      />
    </>
  );
}