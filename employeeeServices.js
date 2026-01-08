// Mock data - replace with your actual API call
const employeeData = [
  {
    "User Code": "VIPL2SP24054",
    "User FirstName": "Yuvarani",
    "User SurName": "Sitharaman",
    "User Email": "Yuvarani@zobble.com",
    "User AlternateEmail": "Yuvarani@zobble.com",
    "Reporting Authority Code": "010J32093",
    "Reporting Authority Name": "Viral",
    "Reporting Authority Email": "Viral@zobble.com",
    "Gender": "Female",
    "User Birthdate": "NA",
    "User Date Of Jog": "18/11/2024",
    "User Date Of Registration": "05/11/2024",
    "User Date Of Deactivation": "NA",
    "User Date Of Expiry": "NA",
    "User Last Log Date": "11/05/2025",
    "UserLogCount": "64",
    "User MobileNumber": "7825849879",
    "PanNumber": "",
    "AdharNumber": "",
    "User Batch Date": "01/01/1900",
    "User Promotion Date": "",
    "User Active": "1",
    "Time Zone": "(GMT+05:30) Chennai, Kolkata, Mumbai, New Delhi",
    "Country": "dia",
    "State": "NA",
    "City": "Chennai",
    "Department": "NA",
    "Designation": "NA",
    "Big4": "NA",
    "Buddy GPN": "290987421",
    "ClientServg": "Yes",
    "Competency": "CNS - RISK - PROCESS & CONTROLS",
    "DeptDesc": "FS EYPL surnc 3-Risk-IA TN",
    "DEPTID": "115297",
    "EmpCategory": "EMP010",
    "EMPLID": "5467703",
    "FDC Level": "Manager",
    "Firm": "Ernst & Young LLP",
    "GPN": "20230089441",
    "GRADE": "1",
    "GUI": "3628980",
    "Hiring Manager GPN": "010J32093",
    "Hiring Source": "Placement Consultant",
    "Hiring Type": "New Hire",
    "HR GPN": "VIPL30523024",
    "HRBAND": "3",
    "IT SPOC GPN": "IT000000005",
    "JOBCODE": "300689",
    "JOBDESC": "Ent_Risk_Mgt-32-1-R-M1",
    "LastCompany": "Dover dia Pvt. Ltd.",
    "Learng SPOC GPN": "NA",
    "LPN": "K67618",
    "MS": "FS",
    "OFFICE": "Chennai - Tidel Park",
    "Onboardg SPOC GPN": "010K41825",
    "ONCONTRACT": "No",
    "OperatgUnit": "Business Consultg Risk",
    "PAYGROUP": "EMP",
    "ProbationConfirmation": "Pending",
    "RANK": "32",
    "Sector": "Banking & Capital Markets",
    "Servicele": "Business Consultg Risk",
    "SubServicele": "NA",
    "Title": "Manager",
    "EMPLOYEETYPE": "Lateral",
    "EmployeeStatus": "Joined",
    "Partner GPN": "010J02202",
    "Talent Leader GPN": "NA",
    "SLLead GPN": "NA",
    "CampusHirg": "NA",
    "Hiring Source Description": "NA",
    "LastUpdatedDate": "17/01/2025",
    "UpdatedTime": "8:44 PM",
    "UpdatedBy": "ExcelImport-Update"
  }
  // ... add all your other employee records here
];

export const employeeService = {
  // Get all employees
  getAllEmployees: () => {
    return Promise.resolve(employeeData);
  },

  // Get employee by User Code
  getEmployeeByCode: (userCode) => {
    const employee = employeeData.find(emp => emp["User Code"] === userCode);
    return Promise.resolve(employee);
  },

  // Search employees by name
  searchEmployees: (searchTerm) => {
    const filtered = employeeData.filter(emp => 
      emp["User FirstName"].toLowerCase().includes(searchTerm.toLowerCase()) ||
      emp["User SurName"].toLowerCase().includes(searchTerm.toLowerCase()) ||
      emp["User Email"].toLowerCase().includes(searchTerm.toLowerCase())
    );
    return Promise.resolve(filtered);
  },

  // Filter employees by criteria
  filterEmployees: (filters) => {
    let filtered = [...employeeData];

    if (filters.city) {
      filtered = filtered.filter(emp => emp.City === filters.city);
    }

    if (filters.department) {
      filtered = filtered.filter(emp => emp.Department === filters.department);
    }

    if (filters.fdcLevel) {
      filtered = filtered.filter(emp => emp["FDC Level"] === filters.fdcLevel);
    }

    if (filters.employeeStatus) {
      filtered = filtered.filter(emp => emp.EmployeeStatus === filters.employeeStatus);
    }

    return Promise.resolve(filtered);
  },

  // Get unique values for filters
  getFilterOptions: () => {
    const cities = [...new Set(employeeData.map(emp => emp.City).filter(city => city !== "NA"))];
    const departments = [...new Set(employeeData.map(emp => emp.Department).filter(dept => dept !== "NA"))];
    const fdcLevels = [...new Set(employeeData.map(emp => emp["FDC Level"]))];
    const employeeStatuses = [...new Set(employeeData.map(emp => emp.EmployeeStatus))];

    return Promise.resolve({
      cities,
      departments,
      fdcLevels,
      employeeStatuses
    });
  }
};
