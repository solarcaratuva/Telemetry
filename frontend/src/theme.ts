import "@mui/material/styles/createPalette";

import { createTheme } from "@mui/material/styles";

declare module "@mui/material/styles/createPalette" {
  interface Palette {
    disabled: Palette["primary"];
  }
  interface PaletteOptions {
    disabled: PaletteOptions["primary"];
  }
}

export const theme = createTheme({
  palette: {
    primary: {
      main: "#082255",
    },
    disabled: {
      main: "#cccccc",
    },
  },
});
