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
import DeleteIcon from '@material-ui/icons/Delete';
import React from 'react';

export default function PriceDataMaintTemplate(state) {
  return (
    <>
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Card>
            <CardHeader title='Import Daily Prices'></CardHeader>
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
        <Grid item xs={4}>
          <Card>
            <CardHeader title='Delete Stock Price Older Than 30 Years'></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container>
                <Grid item xs={12}>
                  <ButtonGroup fullWidth>
                    <Button
                      size='large'
                      variant='contained'
                      color='secondary'
                      onClick={() => state.onClickDelete()}
                      disabled={state.is_processing}
                    >
                      <DeleteIcon />
                      Delete
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
