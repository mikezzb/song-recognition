import { Switch, styled } from '@material-ui/core';
import './Header.scss';

// Reference: https://mui.com/zh/components/switches/
const ModeSwitch = styled(Switch)(({ theme }) => ({
  'width': 62,
  'height': 34,
  'padding': 7,
  '& .MuiSwitch-switchBase': {
    'margin': 1,
    'padding': 0,
    'transform': 'translateX(6px)',
    '&.Mui-checked': {
      'color': '#fff',
      'transform': 'translateX(22px)',
      '& .MuiSwitch-thumb:before': {
        backgroundImage: `url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="0 0 24 24"><path fill="${encodeURIComponent(
          '#fff'
        )}" d="M7 18h2V6H7v12zm4 4h2V2h-2v20zm-8-8h2v-4H3v4zm12 4h2V6h-2v12zm4-8v4h2v-4h-2z"/></svg>')`,
      },
      '& + .MuiSwitch-track': {
        opacity: 1,
        backgroundColor: '#4d5c6a',
      },
    },
  },
  '& .MuiSwitch-thumb': {
    'backgroundColor': '#a70241',
    'width': 32,
    'height': 32,
    '&:before': {
      content: "''",
      position: 'absolute',
      width: '100%',
      height: '100%',
      left: 0,
      top: 0,
      backgroundRepeat: 'no-repeat',
      backgroundPosition: 'center',
      backgroundImage: `url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="0 0 24 24"><path fill="${encodeURIComponent(
        '#fff'
      )}" d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>')`,
    },
  },
  '& .MuiSwitch-track': {
    opacity: 1,
    backgroundColor: '#4d5c6a',
    borderRadius: 20 / 2,
  },
}));

export default ModeSwitch;
