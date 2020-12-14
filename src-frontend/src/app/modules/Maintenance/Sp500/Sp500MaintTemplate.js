import {
  Button,
  ButtonGroup,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  IconButton,
  Snackbar,
} from '@material-ui/core';

import AddIcon from '@material-ui/icons/Add';
import CloseIcon from '@material-ui/icons/Close';
import React from 'react';

export default function Sp500MaintTemplate(state) {
  return (
    <>
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Card>
            <CardHeader title='SP 500 Symbols NOT in DB'></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container>
                <Grid item xs={12}>
                  <ButtonGroup fullWidth>
                    <Button
                      size='large'
                      variant='contained'
                      color='secondary'
                      onClick={() => state.onClickImport()}
                      disabled={state.is_processing}
                    >
                      <AddIcon />
                      Import
                    </Button>
                  </ButtonGroup>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Snackbar
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        open={state.is_snackbar_open}
        autoHideDuration={6000}
        onClose={state.onCloseSnackbar}
        message={<span>{state.snackbar_content}</span>}
        action={[
          <IconButton key='close' aria-label='Close' color='inherit' className='p-1' onClick={state.onCloseSnackbar}>
            <CloseIcon />
          </IconButton>,
        ]}
      />
    </>
  );
}
