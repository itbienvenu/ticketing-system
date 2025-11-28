import axiosClient from "./axiosClient";

export const createTicket = async (payload: any) => {
  const { data } = await axiosClient.post("/tickets", payload);
  return data;
};

export const getTickets = async () => {
  const { data } = await axiosClient.get("/tickets");
  return data;
};

export const updateTicket = async (id: string, payload: any) => {
  const { data } = await axiosClient.patch(`/tickets/${id}`, payload);
  return data;
};

export const deleteTicket = async (id: string) => {
  const { data } = await axiosClient.delete(`/tickets/${id}`);
  return data;
};
