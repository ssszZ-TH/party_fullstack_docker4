import React, { lazy, Suspense } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { ThemeProvider } from "./contexts/ThemeContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Loading from "./components/Loading";

// Lazy load pages เพื่อเพิ่มประสิทธิภาพ
const RootPage = lazy(() => import("./pages/RootPage"));
const AdminLogin = lazy(() => import("./pages/login/AdminLogin"));
const PersonLogin = lazy(() => import("./pages/login/PersonLogin"));
const OrganizationLogin = lazy(() => import("./pages/login/OrganizationLogin"));
const Register = lazy(() => import("./pages/Register"));
const SystemAdminHome = lazy(() => import("./pages/homes/SystemAdminHome"));
const BasetypeAdminHome = lazy(() => import("./pages/homes/BasetypeAdminHome"));
const HrAdminHome = lazy(() => import("./pages/homes/HrAdminHome"));
const OrganizationAdminHome = lazy(() => import("./pages/homes/OrganizationAdminHome"));
const PersonUserHome = lazy(() => import("./pages/homes/PersonUserHome"));
const OrganizationUserHome = lazy(() => import("./pages/homes/OrganizationUserHome"));
const PersonDetail = lazy(() => import("./pages/layer_info/PersonDetail"));
const PassportByCitizenshipId = lazy(() => import("./pages/layer_info/PassportByCitizenshipId"));

// กำหนด array ของ routes สำหรับหน้าเพิ่มเติม
const routes = [
  { path: "/v1/person", component: lazy(() => import("./pages/layer_info/Person")) },
  { path: "/v1/country", component: lazy(() => import("./pages/layer_type/Country")) },
  { path: "/v1/passport", component: lazy(() => import("./pages/layer_info/Passport")) },
  { path: "/v1/passport/:paramId", component: lazy(() => import("./pages/layer_info/PassportDetail")) },
  { path: "/v1/profile", component: lazy(() => import("./pages/Profile")) },
  { path: "/v1/partytype", component: lazy(() => import("./pages/layer_type/PartyType")) },
  { path: "/v1/ethnicity", component: lazy(() => import("./pages/layer_type/Ethnicity")) },
  { path: "/v1/personname", component: lazy(() => import("./pages/layer_info/PersonName")) },
  { path: "/v1/incomerange", component: lazy(() => import("./pages/layer_type/IncomeRange")) },
  { path: "/v1/citizenship", component: lazy(() => import("./pages/layer_info/Citizenship")) },
  { path: "/v1/industrytype", component: lazy(() => import("./pages/layer_type/IndustryType")) },
  { path: "/v1/industrybyorganizationid/:paramId", component: lazy(() => import("./pages/layer_info/IndustryByOrganizationId")) },
  { path: "/v1/sizebyorganizationid/:paramId", component: lazy(() => import("./pages/layer_info/SizeByOrganization")) },
  { path: "/v1/minoritybyorganizationid/:paramId", component: lazy(() => import("./pages/layer_info/MinorityByOrganizationId")) },
  { path: "/v1/minoritytype", component: lazy(() => import("./pages/layer_type/MinorityType")) },
  { path: "/v1/maritalstatus", component: lazy(() => import("./pages/layer_info/MaritalStatus")) },
  { path: "/v1/classifybyeeoc", component: lazy(() => import("./pages/layer_info/ClassifyByeeoc")) },
  { path: "/v1/classifybysize", component: lazy(() => import("./pages/layer_info/ClassifyBySize")) },
  { path: "/v1/personnametype", component: lazy(() => import("./pages/layer_type/PersonNameType")) },
  { path: "/v1/classifybyincome", component: lazy(() => import("./pages/layer_info/ClassifyByIncome")) },
  { path: "/v1/incomedetail/:paramId", component: lazy(() => import("./pages/layer_info/IncomeDetail")) },
  { path: "/v1/classifybyminority", component: lazy(() => import("./pages/layer_info/ClassifyByMinority")) },
  { path: "/v1/classifybyindustry", component: lazy(() => import("./pages/layer_info/ClassifyByIndustry")) },
  { path: "/v1/employeecountrange", component: lazy(() => import("./pages/layer_type/EmployeeCountRange")) },
  { path: "/v1/maritalstatustype", component: lazy(() => import("./pages/layer_type/MaritalStatusType")) },
  { path: "/v1/physicalcharacteristic", component: lazy(() => import("./pages/layer_info/PhysicalCharacteristic")) },
  { path: "/v1/physicalcharacteristictype", component: lazy(() => import("./pages/layer_type/PhysicalCharacteristicType")) },
  { path: "/v1/gendertype", component: lazy(() => import("./pages/layer_type/Gendertype")) },
  { path: "/v1/team", component: lazy(() => import("./pages/layer_type/Team")) },
  { path: "/v1/family", component: lazy(() => import("./pages/layer_type/Family")) },
  { path: "/v1/otherinformalorganization", component: lazy(() => import("./pages/layer_type/OtherInformalOrganization")) },
  { path: "/v1/governmentagency", component: lazy(() => import("./pages/layer_type/GovernmentAgency")) },
  { path: "/v1/corporation", component: lazy(() => import("./pages/layer_type/Corporation")) },
  { path: "/v1/persondetail", component: lazy(() => import("./pages/layer_info/PersonDetail")) },
  { path: "/v1/organizationmenu", component: lazy(() => import("./pages/layer_info/OrganizationMenu")) },
  { path: "/v1/person/:paramId", component: PersonDetail },
  { path: "/v1/passportbycitizenshipid/:paramId", component: PassportByCitizenshipId },
  { path: "/v1/eeocbypersonid/:paramId", component: lazy(() => import("./pages/layer_info/EeocByPersonId")) },
  { path: "/v1/eeocdetail/:paramId", component: lazy(() => import("./pages/layer_info/EeocDetail")) },
  { path: "/v1/incomebypersonid/:paramId", component: lazy(() => import("./pages/layer_info/IncomeByPersonId")) },
  { path: "/v1/organization", component: lazy(() => import("./pages/layer_type/Organization")) },
  { path: "/v1/organization/:param", component: lazy(() => import("./pages/layer_type/Organization")) },
  { path: "/v1/corporation/:paramId", component: lazy(() => import("./pages/layer_type/CorporationDetail")) },
  { path: "/v1/governmentagency/:paramId", component: lazy(() => import("./pages/layer_type/GovernmentAgencyDetail")) },
  { path: "/v1/family/:paramId", component: lazy(() => import("./pages/layer_type/FamilyDetail")) },
  { path: "/v1/otherinformalorganization/:paramId", component: lazy(() => import("./pages/layer_type/OtherInformalOrganizationDetail")) },
  { path: "/v1/team/:paramId", component: lazy(() => import("./pages/layer_type/TeamDetail")) },
  { path: "/v1/organization/create", component: lazy(() => import("./pages/layer_type/OrganizationCreate")) },
  { path: "/v1/industrydetail/:paramId", component: lazy(() => import("./pages/layer_info/IndustryDetail")) },
  { path: "/v1/minoritydetail/:paramId", component: lazy(() => import("./pages/layer_info/MinorityDetail")) },
  { path: "/v1/sizedetail/:paramId", component: lazy(() => import("./pages/layer_info/SizeDetail")) },
  { path: "/v1/communicationeventpurposetype", component: lazy(() => import("./pages/layer_type/CommunicationEventPurposeType")) },
  { path: "/v1/contactmechanismtype", component: lazy(() => import("./pages/layer_type/ContactMechanismType")) },
  { path: "/v1/communicationeventstatustype", component: lazy(() => import("./pages/layer_type/CommunicationEventStatusType")) },
  { path: "/v1/prioritytype", component: lazy(() => import("./pages/layer_type/PriorityType")) },
  { path: "/v1/partyrelationshipstatustype", component: lazy(() => import("./pages/layer_type/PartyRelationshipStatusType")) },
  { path: "/v1/partyrelationshiptype", component: lazy(() => import("./pages/layer_type/PartyRelationshipType")) },
  { path: "/v1/roletype", component: lazy(() => import("./pages/layer_type/RoleType")) },
  { path: "/v1/partyrole", component: lazy(() => import("./pages/layer_role/PartyRole")) },
  { path: "/v1/partyrole/:paramId", component: lazy(() => import("./pages/layer_role/PartyRoleDetail")) },
  { path: "/v1/partyrelationship/", component: lazy(() => import("./pages/layer_relationship/PartyRelationship")) },
  { path: "/v1/partyrelationship/:paramId", component: lazy(() => import("./pages/layer_relationship/PartyRelationshipDetail")) },
  { path: "/v1/communicationevent/", component: lazy(() => import("./pages/layer_commu_event/CommunicationEvent")) },
  { path: "/v1/communicationevent/:paramId", component: lazy(() => import("./pages/layer_commu_event/CommunicationEventDetail")) },
  { path: "/v1/communicationeventpurpose/", component: lazy(() => import("./pages/layer_commu_purpose/CommunicationEventPurpose")) },
  { path: "/v1/communicationeventpurpose/:paramId", component: lazy(() => import("./pages/layer_commu_purpose/CommunicationEventPurposeDetail")) },
];

// Render แอปพลิเคชัน
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Suspense fallback={<Loading />}>
            <Routes>
              <Route path="/login/admin" element={<AdminLogin />} />
              <Route path="/login/person" element={<PersonLogin />} />
              <Route path="/login/organization" element={<OrganizationLogin />} />
              <Route path="/register" element={<Register />} />
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <RootPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/homes/system_admin"
                element={
                  <ProtectedRoute>
                    <SystemAdminHome />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/homes/basetype_admin"
                element={
                  <ProtectedRoute>
                    <BasetypeAdminHome />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/homes/hr_admin"
                element={
                  <ProtectedRoute>
                    <HrAdminHome />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/homes/organization_admin"
                element={
                  <ProtectedRoute>
                    <OrganizationAdminHome />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/homes/person_user"
                element={
                  <ProtectedRoute>
                    <PersonUserHome />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/homes/organization_user"
                element={
                  <ProtectedRoute>
                    <OrganizationUserHome />
                  </ProtectedRoute>
                }
              />
              {routes.map((route) => (
                <Route
                  key={route.path}
                  path={route.path}
                  element={
                    <ProtectedRoute>
                      <route.component />
                    </ProtectedRoute>
                  }
                />
              ))}
              <Route path="*" element={<h1>404 Not Found</h1>} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);