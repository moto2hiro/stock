import * as AppConsts from '../../AppConsts';

import {
  Button,
  ButtonGroup,
  Card,
  CardContent,
  CardHeader,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  IconButton,
  ListItemText,
  MenuItem,
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

import { Chart } from 'react-google-charts';
import CloseIcon from '@material-ui/icons/Close';
import FormUtils from '../../appUtils/FormUtils';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';
import HighlightOffIcon from '@material-ui/icons/HighlightOff';
import React from 'react';
import TrendingUpIcon from '@material-ui/icons/TrendingUp';
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
  fab: {
    margin: theme.spacing(1),
  },
  extendedIcon: {
    marginRight: theme.spacing(1),
  },
  textField: {
    marginBottom: theme.spacing(3),
    width: 200,
    '& .MuiSelect-icon': {
      position: 'relative',
    },
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chip: {
    margin: 2,
  },
  typography: {
    padding: theme.spacing(2),
  },
}));

export default function BackTestTemplate(state) {
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
            <CardHeader title='Set Up'></CardHeader>
            <Divider light={true} />
            <CardContent>
              <Grid container spacing={5}>
                <Grid item sm={6} xs={12} className='mb-5'>
                  <Grid container>
                    <Grid item xs={12}>
                      <h4 className='font-weight-normal'>Portfolio</h4>
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='start_capital'
                        label='Start Capital'
                        value={state.request.start_capital}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='number'
                        inputProps={{ step: 0.01 }}
                        className={classes.textField}
                        error={state.validation.formData.start_capital?.isInvalid}
                        helperText={state.validation.formData.start_capital?.message}
                      />
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='pct_risk_per_trade'
                        label='% to risk per trade'
                        value={state.request.pct_risk_per_trade}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='number'
                        inputProps={{ step: 0.01 }}
                        className={classes.textField}
                        error={state.validation.formData.pct_risk_per_trade?.isInvalid}
                        helperText={state.validation.formData.pct_risk_per_trade?.message}
                      />
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='portfolio_max'
                        label='Portfolio Max'
                        value={state.request.portfolio_max}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='number'
                        inputProps={{ step: 1 }}
                        className={classes.textField}
                        error={state.validation.formData.portfolio_max?.isInvalid}
                        helperText={state.validation.formData.portfolio_max?.message}
                        InputProps={{
                          endAdornment: (
                            <>
                              <IconButton
                                color='secondary'
                                onClick={onOpenPopover('Max # of trades in position at the same time.')}
                                className='p-0'
                              >
                                <HelpOutlineIcon />
                              </IconButton>
                            </>
                          ),
                        }}
                      />
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        select
                        SelectProps={{
                          multiple: true,
                          renderValue: (selected) => (
                            <div className={classes.chips}>
                              {selected.map((value) => (
                                <Chip
                                  key={value}
                                  label={value}
                                  className={classes.chip}
                                  onDelete={() => {}}
                                  deleteIcon={
                                    <HighlightOffIcon
                                      onMouseDown={(event) => {
                                        event.stopPropagation();
                                        state.onDeleteBenchmark(value);
                                      }}
                                    />
                                  }
                                />
                              ))}
                            </div>
                          ),
                        }}
                        name='benchmark_etfs'
                        label='Benchmark ETFs'
                        value={state.request.benchmark_etfs}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        className={classes.textField}
                        error={state.validation.formData.benchmark_etfs?.isInvalid}
                        helperText={state.validation.formData.benchmark_etfs?.message}
                      >
                        <MenuItem value={AppConsts.BENCHMARK_ETF_SPY}>
                          <ListItemText primary={AppConsts.BENCHMARK_ETF_SPY} />
                        </MenuItem>
                        <MenuItem value={AppConsts.BENCHMARK_ETF_DIA}>
                          <ListItemText primary={AppConsts.BENCHMARK_ETF_DIA} />
                        </MenuItem>
                      </TextField>
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='date_from'
                        label='Date From'
                        value={state.request.date_from}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='date'
                        className={classes.textField}
                        error={state.validation.formData.date_from?.isInvalid}
                        helperText={state.validation.formData.date_from?.message}
                      />
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='date_to'
                        label='Date To'
                        value={state.request.date_to}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='date'
                        className={classes.textField}
                        error={state.validation.formData.date_to?.isInvalid}
                        helperText={state.validation.formData.date_to?.message}
                      />
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='slippage'
                        label='Slippage'
                        value={state.request.slippage}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='number'
                        inputProps={{ step: 1 }}
                        className={classes.textField}
                        error={state.validation.formData.slippage?.isInvalid}
                        helperText={state.validation.formData.slippage?.message}
                        InputProps={{
                          endAdornment: (
                            <>
                              <IconButton
                                color='secondary'
                                onClick={onOpenPopover('Slippage in basis points (1% = 100bps).')}
                                className='p-0'
                              >
                                <HelpOutlineIcon />
                              </IconButton>
                            </>
                          ),
                        }}
                      />
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='volume_limit'
                        label='Volume Limit'
                        value={state.request.volume_limit}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='number'
                        inputProps={{ step: 0.01 }}
                        className={classes.textField}
                        error={state.validation.formData.volume_limit?.isInvalid}
                        helperText={state.validation.formData.volume_limit?.message}
                        InputProps={{
                          endAdornment: (
                            <>
                              <IconButton
                                color='secondary'
                                onClick={onOpenPopover('Limit the # of shares to trade by % of daily volume.')}
                                className='p-0'
                              >
                                <HelpOutlineIcon />
                              </IconButton>
                            </>
                          ),
                        }}
                      />
                    </Grid>
                    <Grid item md={6} sm={12} xs={12}>
                      <TextField
                        name='test_limit_symbol'
                        label='Test Symbol Limit'
                        value={state.request.test_limit_symbol}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        type='number'
                        inputProps={{ step: 1 }}
                        className={classes.textField}
                        error={state.validation.formData.test_limit_symbol?.isInvalid}
                        helperText={state.validation.formData.test_limit_symbol?.message}
                      />
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item sm={6} xs={12}>
                  <Grid item xs={12}>
                    <h4 className='font-weight-normal'>Strategy</h4>
                  </Grid>
                  <Grid container>
                    <Grid item xs={12}>
                      <TextField
                        select
                        name='strategy_type'
                        label='Strategy Type'
                        value={state.request.strategy_type}
                        onChange={state.onChangeRequest}
                        onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                        className={classes.textField}
                        error={state.validation.formData.strategy_type?.isInvalid}
                        helperText={state.validation.formData.strategy_type?.message}
                        InputProps={{
                          endAdornment: (
                            <>
                              <IconButton
                                color='secondary'
                                onClick={onOpenPopover(state.current_strategy_config?.description)}
                                className='p-0'
                              >
                                <HelpOutlineIcon />
                              </IconButton>
                            </>
                          ),
                        }}
                      >
                        {Object.keys(AppConsts.STRATEGY_CONFIG).map((item) => {
                          return (
                            <MenuItem key={item} value={item}>
                              {AppConsts.STRATEGY_CONFIG[item].label}
                            </MenuItem>
                          );
                        })}
                      </TextField>
                    </Grid>
                    {state.current_strategy_config.fields?.map((field, idx) => {
                      return (
                        <Grid item xs={12} key={idx}>
                          <TextField
                            name={`strategy_request.${field.name}`}
                            label={field.label}
                            value={state.request.strategy_request[field?.name]}
                            onChange={state.onChangeRequest}
                            onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                            type={field.type}
                            className={classes.textField}
                            error={
                              state.validation.formData.strategy_request &&
                              state.validation.formData.strategy_request.formData &&
                              state.validation.formData.strategy_request.formData.hasOwnProperty(field.name) &&
                              state.validation.formData.strategy_request.formData[field.name]?.isInvalid
                            }
                            helperText={
                              !state.validation.formData.strategy_request ||
                              !state.validation.formData.strategy_request.formData ||
                              !state.validation.formData.strategy_request.formData.hasOwnProperty(field.name)
                                ? ''
                                : state.validation.formData.strategy_request.formData[field.name]?.message
                            }
                            inputProps={{ step: field.step }}
                            InputProps={{
                              endAdornment: (
                                <>
                                  {field.description ? (
                                    <IconButton
                                      color='secondary'
                                      onClick={onOpenPopover(field.description)}
                                      className='p-0'
                                    >
                                      <HelpOutlineIcon />
                                    </IconButton>
                                  ) : (
                                    <></>
                                  )}
                                </>
                              ),
                            }}
                          />
                        </Grid>
                      );
                    })}
                  </Grid>
                </Grid>
              </Grid>
            </CardContent>
            <CardContent>
              <Grid container>
                <Grid item xs={12}>
                  <h4 className='font-weight-normal'>Other</h4>
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='adv_min'
                    label='Min ADV'
                    value={state.request.adv_min}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 1 }}
                    className={classes.textField}
                    error={state.validation.formData.adv_min?.isInvalid}
                    helperText={state.validation.formData.adv_min?.message}
                    InputProps={{
                      endAdornment: (
                        <>
                          <IconButton
                            color='secondary'
                            onClick={onOpenPopover('Min average daily volume over the last 50 periods.')}
                            className='p-0'
                          >
                            <HelpOutlineIcon />
                          </IconButton>
                        </>
                      ),
                    }}
                  />
                </Grid>
                <Grid item lg={3} md={6} sm={12} xs={12}>
                  <TextField
                    name='adpv_min'
                    label='Min ADPV'
                    value={state.request.adpv_min}
                    onChange={state.onChangeRequest}
                    onBlur={(e) => FormUtils.onBlurField(e, state.onBlurRequest)}
                    type='number'
                    inputProps={{ step: 0.01 }}
                    className={classes.textField}
                    error={state.validation.formData.adpv_min?.isInvalid}
                    helperText={state.validation.formData.adpv_min?.message}
                    InputProps={{
                      endAdornment: (
                        <>
                          <IconButton
                            color='secondary'
                            onClick={onOpenPopover('Min average daily price volume over the last 50 periods.')}
                            className='p-0'
                          >
                            <HelpOutlineIcon />
                          </IconButton>
                        </>
                      ),
                    }}
                  />
                </Grid>
              </Grid>
            </CardContent>
            <CardContent>
              <Grid container>
                <Grid item xs={12}>
                  <ButtonGroup fullWidth>
                    <Button
                      size='large'
                      variant='contained'
                      color='secondary'
                      onClick={state.onClickRunBackTest}
                      disabled={state.is_processing}
                    >
                      <TrendingUpIcon className={classes.extendedIcon} />
                      Run Back Test
                    </Button>
                  </ButtonGroup>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        {state.has_run_back_test === true && (
          <Grid item xs={12} className='mt-5'>
            <Card>
              <CardHeader title='Results' className='resultsDiv'></CardHeader>
              <Divider light={true} />
              <CardContent>
                {state.is_processing ? (
                  <Grid container justify='center'>
                    <Grid item xs={12} align='center'>
                      <CircularProgress />
                    </Grid>
                  </Grid>
                ) : !state.results?.length ? (
                  <Grid container justify='center'>
                    <Grid item xs={12} align='center'>
                      No results found.
                    </Grid>
                  </Grid>
                ) : (
                  <Grid container>
                    <Grid item xs={12}>
                      <Paper className={classes.paper}>
                        <Table className={classes.table} size='small'>
                          <TableHead>
                            <TableRow>
                              <TableCell colSpan={13} align='center'>
                                Overall Results
                              </TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell>Target</TableCell>
                              <TableCell>End Capital</TableCell>
                              <TableCell>&Delta; in Capital</TableCell>
                              <TableCell>% Return</TableCell>
                              <TableCell>Max W</TableCell>
                              <TableCell>Max L</TableCell>
                              <TableCell>Avg W/L</TableCell>
                              <TableCell>% W</TableCell>
                              <TableCell># of Days</TableCell>
                              <TableCell># of Trades</TableCell>
                              <TableCell>Max Hold</TableCell>
                              <TableCell>Min Hold</TableCell>
                              <TableCell>Avg Hold</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {state.results.map((result, idx) => {
                              return (
                                <TableRow key={idx}>
                                  <TableCell align='left'>{result.target}</TableCell>
                                  <TableCell align='right'>{result.end_capital}</TableCell>
                                  <TableCell align='right'>{result.change_in_capital_stats?.sum}</TableCell>
                                  <TableCell align='right'>{result.pct_return}</TableCell>
                                  <TableCell align='right'>{result.change_in_capital_stats?.max}</TableCell>
                                  <TableCell align='right'>{result.change_in_capital_stats?.min}</TableCell>
                                  <TableCell align='right'>{result.change_in_capital_stats?.mean}</TableCell>
                                  <TableCell align='right'>{result.has_profit_stats?.mean}</TableCell>
                                  <TableCell align='right'>{result.ttl_no_days}</TableCell>
                                  <TableCell align='right'>{result.transactions?.length}</TableCell>
                                  <TableCell align='right'>{result.hold_length_days_stats?.max} days</TableCell>
                                  <TableCell align='right'>{result.hold_length_days_stats?.min} days</TableCell>
                                  <TableCell align='right'>{result.hold_length_days_stats?.mean} days</TableCell>
                                </TableRow>
                              );
                            })}
                          </TableBody>
                        </Table>
                      </Paper>
                    </Grid>
                    <Grid item xs={12}>
                      <Paper className={classes.paper}>
                        <Table className={classes.table} size='small'>
                          <TableHead>
                            <TableRow>
                              <TableCell colSpan={13} align='center'>
                                Best Winning Trades
                              </TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell></TableCell>
                              <TableCell>Symbol</TableCell>
                              <TableCell>Name</TableCell>
                              <TableCell>Sector</TableCell>
                              <TableCell>Industry</TableCell>
                              <TableCell>&Delta; in Capital</TableCell>
                              <TableCell align='center'>Start Date</TableCell>
                              <TableCell align='center'>End Date</TableCell>
                              <TableCell>Start Price</TableCell>
                              <TableCell>End Price</TableCell>
                              <TableCell>&Delta; in Price</TableCell>
                              <TableCell># of Shares</TableCell>
                              <TableCell align='right'>Hold Length</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {state.results
                              .filter((r) => !r.is_benchmark)[0]
                              .best_transactions.map((transaction, idx) => {
                                return (
                                  <TableRow key={idx}>
                                    <TableCell align='left'>{idx + 1}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.symbol}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.name}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.sector}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.industry}</TableCell>
                                    <TableCell align='right'>{transaction.change_in_capital}</TableCell>
                                    <TableCell align='left'>{transaction.start_date}</TableCell>
                                    <TableCell align='left'>{transaction.end_date}</TableCell>
                                    <TableCell align='right'>{transaction.start_price}</TableCell>
                                    <TableCell align='right'>{transaction.end_price}</TableCell>
                                    <TableCell align='right'>{transaction.net_change_in_price}</TableCell>
                                    <TableCell align='right'>{transaction.no_of_shares}</TableCell>
                                    <TableCell align='right'>{transaction.hold_length_days} days</TableCell>
                                  </TableRow>
                                );
                              })}
                          </TableBody>
                        </Table>
                      </Paper>
                    </Grid>
                    <Grid item xs={12}>
                      <Paper className={classes.paper}>
                        <Table className={classes.table} size='small'>
                          <TableHead>
                            <TableRow>
                              <TableCell colSpan={13} align='center'>
                                Worst Losing Trades
                              </TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell></TableCell>
                              <TableCell>Symbol</TableCell>
                              <TableCell>Name</TableCell>
                              <TableCell>Sector</TableCell>
                              <TableCell>Industry</TableCell>
                              <TableCell>&Delta; in Capital</TableCell>
                              <TableCell align='center'>Start Date</TableCell>
                              <TableCell align='center'>End Date</TableCell>
                              <TableCell>Start Price</TableCell>
                              <TableCell>End Price</TableCell>
                              <TableCell>&Delta; in Price</TableCell>
                              <TableCell># of Shares</TableCell>
                              <TableCell align='right'>Hold Length</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {state.results
                              .filter((r) => !r.is_benchmark)[0]
                              .worst_transactions.map((transaction, idx) => {
                                return (
                                  <TableRow key={idx}>
                                    <TableCell align='left'>{idx + 1}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.symbol}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.name}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.sector}</TableCell>
                                    <TableCell align='left'>{transaction.symbol_master?.industry}</TableCell>
                                    <TableCell align='right'>{transaction.change_in_capital}</TableCell>
                                    <TableCell align='left'>{transaction.start_date}</TableCell>
                                    <TableCell align='left'>{transaction.end_date}</TableCell>
                                    <TableCell align='right'>{transaction.start_price}</TableCell>
                                    <TableCell align='right'>{transaction.end_price}</TableCell>
                                    <TableCell align='right'>{transaction.net_change_in_price}</TableCell>
                                    <TableCell align='right'>{transaction.no_of_shares}</TableCell>
                                    <TableCell align='right'>{transaction.hold_length_days} days</TableCell>
                                  </TableRow>
                                );
                              })}
                          </TableBody>
                        </Table>
                      </Paper>
                    </Grid>
                    <Grid item xs={12}>
                      <Paper className={classes.paper}>
                        <Table className={classes.table} size='small'>
                          <TableHead>
                            <TableRow>
                              <TableCell colSpan={7} align='center'>
                                Best Winning Symbols
                              </TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell></TableCell>
                              <TableCell>Symbol</TableCell>
                              <TableCell>Name</TableCell>
                              <TableCell>Sector</TableCell>
                              <TableCell>Industry</TableCell>
                              <TableCell align='right'>&Delta; in Capital</TableCell>
                              <TableCell align='right'># of Transactions</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {state.results
                              .filter((r) => !r.is_benchmark)[0]
                              .best_symbols.map((s, idx) => {
                                return (
                                  <TableRow key={idx}>
                                    <TableCell align='left'>{idx + 1}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.symbol}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.name}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.sector}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.industry}</TableCell>
                                    <TableCell align='right'>{s.change_in_capital}</TableCell>
                                    <TableCell align='right'>{s.no_of_transactions}</TableCell>
                                  </TableRow>
                                );
                              })}
                          </TableBody>
                        </Table>
                      </Paper>
                    </Grid>

                    <Grid item xs={12}>
                      <Paper className={classes.paper}>
                        <Table className={classes.table} size='small'>
                          <TableHead>
                            <TableRow>
                              <TableCell colSpan={7} align='center'>
                                Worst Losing Symbols
                              </TableCell>
                            </TableRow>
                            <TableRow>
                              <TableCell></TableCell>
                              <TableCell>Symbol</TableCell>
                              <TableCell>Name</TableCell>
                              <TableCell>Sector</TableCell>
                              <TableCell>Industry</TableCell>
                              <TableCell align='right'>&Delta; in Capital</TableCell>
                              <TableCell align='right'># of Transactions</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {state.results
                              .filter((r) => !r.is_benchmark)[0]
                              .worst_symbols.map((s, idx) => {
                                return (
                                  <TableRow key={idx}>
                                    <TableCell align='left'>{idx + 1}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.symbol}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.name}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.sector}</TableCell>
                                    <TableCell align='left'>{s.symbol_master?.industry}</TableCell>
                                    <TableCell align='right'>{s.change_in_capital}</TableCell>
                                    <TableCell align='right'>{s.no_of_transactions}</TableCell>
                                  </TableRow>
                                );
                              })}
                          </TableBody>
                        </Table>
                      </Paper>
                    </Grid>
                    <Grid item xs={12}>
                      {state.chart_data && (
                        <Chart
                          width={'100%'}
                          height={'600px'}
                          chartType={AppConsts.GOOGLE_CHART_TYPE_LINE}
                          data={state.chart_data}
                        />
                      )}
                    </Grid>
                  </Grid>
                )}
              </CardContent>
            </Card>
          </Grid>
        )}
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
    </>
  );
}
