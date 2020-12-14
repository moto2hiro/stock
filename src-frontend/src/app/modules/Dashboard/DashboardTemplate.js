import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  Grid,
  IconButton,
  Paper,
  Snackbar,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from '@material-ui/core';

import CloseIcon from '@material-ui/icons/Close';
import LaunchIcon from '@material-ui/icons/Launch';
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  paper: {
    width: '100%',
    overflow: 'auto',
  },
  table: {
    minWidth: 300,
    tableLayout: 'fixed',
  },
}));

export default function DashboardTemplate(state) {
  const classes = useStyles();

  return (
    <>
      <Grid container spacing={2}>
        <Grid item lg={4} md={4} sm={12} xs={12}>
          <Card>
            <CardHeader
              title='Account'
              action={
                <IconButton onClick={() => window.open('https://app.alpaca.markets/paper/dashboard/overview')}>
                  <LaunchIcon />
                </IconButton>
              }
            ></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container>
                <Grid item xs={12}>
                  <Paper className={classes.paper}>
                    <Table className={classes.table} size='small' stickyHeader>
                      <TableBody>
                        {!state.account ? (
                          <TableRow>
                            <TableCell align='center'>No results found.</TableCell>
                          </TableRow>
                        ) : (
                          Object.entries(state.account).map(([key, value]) => {
                            return ![
                              'account_number',
                              'buying_power',
                              'portfolio_value',
                              'equity',
                              'multiplier',
                              'status',
                              'trade_suspended_by_user',
                              'trading_blocked',
                              'shorting_enabled',
                              'account_blocked',
                            ].includes(key) ? null : (
                              <TableRow key={key}>
                                <TableCell align='left'>{key}:</TableCell>
                                <TableCell align='right'>{value !== null ? value.toString() : ''}</TableCell>
                              </TableRow>
                            );
                          })
                        )}
                      </TableBody>
                    </Table>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        <Grid item lg={4} md={4} sm={12} xs={12}>
          <Card>
            <CardHeader title='Active Orders'></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container>
                <Grid item xs={12}>
                  <Paper className={classes.paper}>
                    <Table className={classes.table} size='small' stickyHeader>
                      <TableHead>
                        <TableRow>
                          <TableCell></TableCell>
                          <TableCell>Id</TableCell>
                          <TableCell>Symbol</TableCell>
                          <TableCell>Name</TableCell>
                          <TableCell>Status</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {!state.orders?.length ? (
                          <TableRow>
                            <TableCell colSpan={5} align='center'>
                              No results found.
                            </TableCell>
                          </TableRow>
                        ) : (
                          state.orders.map((o, idx) => {
                            return (
                              <TableRow key={idx}>
                                <TableCell align='left'>{idx + 1}</TableCell>
                                <TableCell align='left'>{o.trade_order.id}</TableCell>
                                <TableCell align='left'>{o.symbol_master.symbol}</TableCell>
                                <TableCell align='left'>{o.symbol_master.name}</TableCell>
                                <TableCell align='left'>{o.trade_order.status}</TableCell>
                              </TableRow>
                            );
                          })
                        )}
                      </TableBody>
                    </Table>
                  </Paper>
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
