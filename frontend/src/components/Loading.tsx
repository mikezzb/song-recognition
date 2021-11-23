import CircularProgress from '@material-ui/core/CircularProgress';
import clsx from 'clsx';
import { FC } from 'react';

import './Loading.scss';

type LoadingProps = {
  fixed?: boolean;
};

const Loading: FC<LoadingProps> = ({ fixed, ...props }) => {
  return (
    <div className={clsx('loading-view', fixed && 'fixed')}>
      <CircularProgress color="secondary" {...props} />
    </div>
  );
};

export default Loading;
