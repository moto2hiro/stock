import * as AppConsts from '../../../AppConsts';

import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  IconButton,
  Paper,
  Popover,
  Snackbar,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@material-ui/core';

import CloseIcon from '@material-ui/icons/Close';
import DateUtils from '../../../appUtils/DateUtils';
import FormUtils from '../../../appUtils/FormUtils';
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  paper: {
    width: '100%',
    overflowX: 'auto',
    marginBottom: theme.spacing(2),
  },
  table: {
    minWidth: 650,
  },
  modalTable: {
    minWidth: 300,
  },
  extendedIcon: {
    marginRight: theme.spacing(1),
  },
  created: {
    marginTop: theme.spacing(2),
  },
  typography: {
    padding: theme.spacing(2),
  },
  dialog: {
    minWidth: 800,
  },
  green: {
    color: 'green',
  },
  orange: {
    color: 'orange',
  },
  red: {
    color: 'red',
  },
}));

export default function TradeSuggestionsTemplate(state) {
  const classes = useStyles();
  const [popoverAnchorEl, setPopoverAnchorEl] = React.useState(null);
  const [isPopoverOpen, setPopoverOpen] = React.useState(false);
  const [popoverContent, setPopoverContent] = React.useState(false);
  const onOpenPopover = (content) => (event) => {
    setPopoverAnchorEl(event.currentTarget);
    setPopoverOpen((prev) => !prev);
    setPopoverContent(content);
  };
  const onClosePopover = (event) => {
    setPopoverAnchorEl(null);
    setPopoverOpen((prev) => !prev);
    setPopoverContent('');
  };

  return (
    <>
      <Grid container>
        <Grid item xs={12}>
          <Card>
            <CardHeader
              title='Trade Suggestions'
              action={
                <TextField
                  name='created'
                  label='Created'
                  value={state.created}
                  onChange={state.onChangeRequest}
                  onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                  type='date'
                  className={classes.created}
                />
              }
            ></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container spacing={5}>
                <Grid item xs={12} className='mb-5'>
                  <Grid container>
                    <Grid item xs={12}>
                      <Paper className={classes.paper}>
                        <Table className={classes.table} size='small'>
                          <TableHead>
                            <TableRow>
                              <TableCell></TableCell>
                              <TableCell>Symbol</TableCell>
                              <TableCell>Company</TableCell>
                              <TableCell>Sector</TableCell>
                              <TableCell>Industry</TableCell>
                              <TableCell>Strategy</TableCell>
                              <TableCell>Status</TableCell>
                              <TableCell>Action</TableCell>
                              <TableCell>Qty</TableCell>
                              <TableCell>Close Price</TableCell>
                              <TableCell>Target Price</TableCell>
                              <TableCell>Stop Loss</TableCell>
                              <TableCell>Created</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {!state.results.length ? (
                              <TableRow>
                                <TableCell colSpan={12} align='center'>
                                  No results found
                                </TableCell>
                              </TableRow>
                            ) : (
                              state.results.map((result, idx) => {
                                return (
                                  <TableRow key={idx}>
                                    <TableCell align='left'>{idx + 1}</TableCell>
                                    <TableCell align='left'>
                                      <Button
                                        color='secondary'
                                        onClick={() => state.onClickSymbol(result.symbol_master.symbol)}
                                      >
                                        {result.symbol_master.symbol}
                                      </Button>
                                    </TableCell>
                                    <TableCell align='left'>{result.symbol_master.name}</TableCell>
                                    <TableCell align='left'>{result.symbol_master.sector}</TableCell>
                                    <TableCell align='left'>{result.symbol_master.industry}</TableCell>
                                    <TableCell align='left'>{result.trade_order.strategy}</TableCell>
                                    <TableCell align='right'>{result.trade_order.status}</TableCell>
                                    <TableCell align='left'>{result.trade_order.action}</TableCell>
                                    <TableCell align='right'>{result.trade_order.qty}</TableCell>
                                    <TableCell align='right'>{result.stock_price_daily.close_price}</TableCell>
                                    <TableCell align='right'>{result.trade_order.target_price}</TableCell>
                                    <TableCell align='right'>{result.trade_order.stop_loss}</TableCell>
                                    <TableCell>
                                      {DateUtils.toYYYY_MM_DD(new Date(result.trade_order.created))}
                                    </TableCell>
                                  </TableRow>
                                );
                              })
                            )}
                          </TableBody>
                        </Table>
                      </Paper>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Popover
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={isPopoverOpen}
        anchorEl={popoverAnchorEl}
        onClose={onClosePopover}
      >
        {<Typography className={classes.typography}>{popoverContent}</Typography>}
      </Popover>
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
      <Dialog open={state.is_modal_open} onClose={state.onCloseModal} scroll='paper' maxWidth='xl'>
        <DialogTitle>{state.key_info.symbol}</DialogTitle>
        <DialogContent dividers={true}>
          <Grid container spacing={2}>
            {!state.has_key_info ? (
              ''
            ) : (
              <>
                <Grid item xs={6}>
                  <Table className={classes.modalTable} size='small'>
                    <TableBody>
                      <TableRow>
                        <TableCell align='left'>Market Cap (In Millions)</TableCell>
                        <TableCell
                          align='right'
                          className={
                            state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.marketCap *
                              1000000 >
                            AppConsts.MARKET_CAP_MIN_DFLT
                              ? classes.green
                              : classes.red
                          }
                        >
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.marketCap}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>52 Week High</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.high52}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>52 Week Low</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.low52}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Vol. 10 Day Avg.</TableCell>
                        <TableCell
                          align='right'
                          className={
                            state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.vol10DayAvg >
                            AppConsts.ADV_MIN_DFLT
                              ? classes.green
                              : classes.red
                          }
                        >
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.vol10DayAvg}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Vol. 3 Month Avg.</TableCell>
                        <TableCell
                          align='right'
                          className={
                            state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.vol3MonthAvg >
                            AppConsts.ADV_MIN_DFLT
                              ? classes.green
                              : classes.red
                          }
                        >
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.vol3MonthAvg}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>PE Ratio</TableCell>
                        <TableCell
                          align='right'
                          className={
                            state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.peRatio <
                            AppConsts.PE_RATIO_IDEAL_DFLT
                              ? classes.green
                              : state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.peRatio <
                                AppConsts.PE_RATIO_MAX_DFLT
                              ? classes.orange
                              : classes.red
                          }
                        >
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.peRatio}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>PB Ratio</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.pbRatio}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Current Ratio</TableCell>
                        <TableCell
                          align='right'
                          className={
                            state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.currentRatio >
                            AppConsts.CURRENT_RATIO_MIN_DFLT
                              ? classes.green
                              : classes.red
                          }
                        >
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.currentRatio}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Beta</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.beta}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </Grid>
                <Grid item xs={6}>
                  <Table className={classes.modalTable} size='small'>
                    <TableBody>
                      <TableRow>
                        <TableCell align='left'>Gross Margin TTM</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.grossMarginTTM}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Net Profit Margin TTM</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.netProfitMarginTTM}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Operating Margin TTM</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.operatingMarginTTM}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>EPS TTM</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.epsTTM}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>EPS Change Pct TTM</TableCell>
                        <TableCell align='right'>
                          {
                            state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental
                              .epsChangePercentTTM
                          }
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>ROE</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.returnOnEquity}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>ROA</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.returnOnAssets}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Total Debt To Equity</TableCell>
                        <TableCell align='right'>
                          {state.key_info.td_ameritrade_key_stats[state.key_info.symbol].fundamental.totalDebtToEquity}
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell align='left'>Next Earnings Date</TableCell>
                        <TableCell
                          align='right'
                          className={
                            DateUtils.getDiffInDays(
                              new Date(),
                              new Date(state.key_info.iex_cloud_key_stats.nextEarningsDate)
                            ) > 5
                              ? classes.green
                              : classes.red
                          }
                        >
                          {state.key_info.iex_cloud_key_stats.nextEarningsDate}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </Grid>
                <Grid item xs={12}>
                  <Table className={classes.modalTable} size='small'>
                    <TableHead>
                      <TableRow>
                        <TableCell colSpan={5} align='center'>
                          News
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Source</TableCell>
                        <TableCell>Content</TableCell>
                        <TableCell>Related</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {state.key_info.news.iex_cloud.map((item, idx) => {
                        return (
                          <TableRow key={idx}>
                            <TableCell>{DateUtils.toYYYY_MM_DD(new Date(item.datetime))}</TableCell>
                            <TableCell>
                              <a href={item.url} target='_blank' rel='noopener noreferrer'>
                                {item.source}
                              </a>
                            </TableCell>
                            <TableCell>
                              Title: {item.headline} <br />
                              Summary: {item.summary}
                            </TableCell>
                            <TableCell>{item.related}</TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </Grid>
              </>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={state.onCloseModal} color='secondary'>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
