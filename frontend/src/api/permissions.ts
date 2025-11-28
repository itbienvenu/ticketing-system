import axiosClient from "./axiosClient";

export const getRoles = async () => {
  const { data } = await axiosClient.get("/roles");
  return data;
};

export const updateRolePermissions = async (roleId: string, permissions: string[]) => {
  const { data } = await axiosClient.patch(`/roles/${roleId}/permissions`, {
    permissions,
  });
  return data;
};
