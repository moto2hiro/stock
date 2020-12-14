import Button from '@material-ui/core/Button';
import React from 'react';
import Tooltip from '@material-ui/core/Tooltip';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

const HtmlTooltip = withStyles((theme) => ({
  tooltip: {
    backgroundColor: '#f5f5f9',
    color: 'rgba(0, 0, 0, 0.87)',
    maxWidth: 220,
    fontSize: theme.typography.pxToRem(12),
    border: '1px solid #dadde9',
  },
}))(Tooltip);

export default function CustomToolTip(state) {
  return (
    <>
      <HtmlTooltip
        title={
          <React.Fragment>
            <Typography color='inherit'>{state.title}</Typography>
            {state.description}
          </React.Fragment>
        }
      >
        {state.content}
      </HtmlTooltip>
    </>
  );
}
